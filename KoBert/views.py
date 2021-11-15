import os

from rest_framework.views import APIView
from django.http import JsonResponse
from . import models
class GetEmotion(APIView):
    def post(self, request):

        message = request.data.get('message')

        dir_path = os.getcwd()
        model_path = os.path.join(dir_path, "\KoBERT")

        emotion =[]
        emotion.append(dict(emotion=models.predict(message)))

        #print(emotion)
        return JsonResponse(dict(emotion=models.predict(message)))

'''
놀람 = 0
분노 = 1
불안 = 2
슬픔 = 3
중립 = 4
행복 = 5
'''