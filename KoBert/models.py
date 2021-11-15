from django.db import models

import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as aoptim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

import os
import pandas as pd

print(os.getcwd())
dir_path = os.getcwd()
data_name = "data.xlsx"
model_name = "classifier.pt"

data_path = os.path.join(dir_path, data_name)
model_path = os.path.join(dir_path, model_name)

chatbot_data = pd.read_excel(data_path, engine='openpyxl')



bertmodel, vocab = get_pytorch_kobert_model()
device = torch.device("cpu")



chatbot_data.loc[(chatbot_data['Emotion'] == "놀람"), 'Emotion'] = 0  #놀람 0
chatbot_data.loc[(chatbot_data['Emotion'] == "분노"), 'Emotion'] = 1  #분노 1
chatbot_data.loc[(chatbot_data['Emotion'] == "불안"), 'Emotion'] = 2  #불안 2
chatbot_data.loc[(chatbot_data['Emotion'] == "슬픔"), 'Emotion'] = 3  #슬픔 3
chatbot_data.loc[(chatbot_data['Emotion'] == "중립"), 'Emotion'] = 4  #중립 4
chatbot_data.loc[(chatbot_data['Emotion'] == "행복"), 'Emotion'] = 5  #행복 5

data_list = []
for q, label in zip(chatbot_data['Sentence'], chatbot_data['Emotion']):
  data = []
  data.append(q)
  data.append(str(label))
  data_list.append(data)


#train_test_split 라이브러리(학습/평가데이터 나누기 (5:1 비율))
from sklearn.model_selection import train_test_split

dataset_train, dataset_test = train_test_split(data_list, test_size = 0.2, random_state=0)

print(len(dataset_train))
print(len(dataset_test))


class BERTDataset(Dataset):
  def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
    transform = nlp.data.BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
    self.sentences = [transform([i[sent_idx]]) for i in dataset]
    self.labels = [np.int32(i[label_idx]) for i in dataset]

  def __getitem__(self, i):
    return (self.sentences[i] + (self.labels[i],))

  def __len__(self):
    return (len(self.labels))


max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 3
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5


tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
data_test = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)

#data_train[0]


train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, num_workers=0)
test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size, num_workers=0)


class BERTClassifier(nn.Module):
  def __init__(self, bert, hidden_size=768, num_classes=6, dr_rate=None, params=None):
    super(BERTClassifier, self).__init__()
    self.bert = bert
    self.dr_rate = dr_rate
    self.classifier = nn.Linear(hidden_size, num_classes)

    if dr_rate:
      self.dropout = nn.Dropout(p=dr_rate)

  def gen_attention_mask(self, token_ids, valid_length):
    attention_mask = torch.zeros_like(token_ids)

    for i, v in enumerate(valid_length):
      attention_mask[i][:v] = 1

    return attention_mask.float()

  def forward(self, token_ids, valid_length, segment_ids):
    attention_mask = self.gen_attention_mask(token_ids, valid_length)
    _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                          attention_mask=attention_mask.float().to(token_ids.device))

    if self.dr_rate:
      out = self.dropout(pooler)

      return self.classifier(out)




model = BERTClassifier(bertmodel, dr_rate=0.5).to(device)

no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [{'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
                                {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}]
optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()

t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total*warmup_ratio)

scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

def calc_accuracy(X, Y):
  max_vals, max_indices = torch.max(X,1)
  train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]

  return train_acc

train_dataloader



#여기서 load
#model_save_name = 'classifier.pt'
#path = F"/Users/sohyeon/Desktop/test_model/{model_save_name}"
#model.load_state_dict(torch.load(path))
model.load_state_dict(torch.load(model_path, map_location=device))

#device = torch.device('cpu')
#model = BERTClassifier()
#model.load_state_dict(torch.load(path, map_location=device))
#model.load_state_dict(torch.load(path, map_location=device),strict=False)
#device = torch.device('cpu')
#model = load_state_dict(torch.load('EmotionClassifier1.pt', map_location=device))


tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower = False)

def predict(predict_sentence):
  data = [predict_sentence, '0']
  dataset_another = [data]

  another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
  test_dataloader = torch.utils.data.DataLoader(another_test, batch_size = batch_size, num_workers = 0)

  model.eval()

  for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
    token_ids = token_ids.long().to(device)
    segment_ids = segment_ids.long().to(device)
    valid_length = valid_length
    label = label.long().to(device)

    out = model(token_ids, valid_length, segment_ids)

    test_eval = []
    for i in out:
      logits = i
      logits = logits.detach().cpu().numpy()

      if np.argmax(logits) == 0:
        test_eval.append("0")
      elif np.argmax(logits) == 1:
        test_eval.append("1")
      elif np.argmax(logits) == 2:
        test_eval.append("2")
      elif np.argmax(logits) == 3:
        test_eval.append("3")
      elif np.argmax(logits) == 4:
        test_eval.append("4")
      elif np.argmax(logits) == 5:
        test_eval.append("5")

    print("->입력한 문장의 감정:" + test_eval[0])
    return test_eval[0]

'''
while True:
  sentence = input('입력문장(없으면 no): ')
  if sentence == 'no':
    break
  predict(sentence)
  print('\n')
'''