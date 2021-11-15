from django.shortcuts import render
from rest_framework.views import APIView
from chatting.models import User_Chat
from chatting.models import Chat
from chattingroom.models import Msg
from login_signup.models import User
from friends.models import user_friend
from django.http import JsonResponse

# Create your views here.

class getChatting(APIView):
    def post(self, request):

        user_id = request.data.get('user_id')
        other_user_id = request.data.get('other_user_id')
        chat_index = request.data.get('chat_index')

        #chat_index로 msg 테이블에서 해당 채팅방에 해당되는 메시지 중 사용자 메시지 가져오기
        user_msg_list = []
        user_msg_db_list = Msg.objects.filter(msg_user_id=user_id,msg_chat_index=chat_index).all()

        for user_msg in user_msg_db_list:
            user_msg_list.append(user_msg.msg_text)


        return JsonResponse()



class sendMessage(APIView):
    def post(self,request):

        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        chat_index = request.data.get('chat_index')



        return JsonResponse()



class getMessage(APIView):
    def post(self,request):

        return JsonResponse()




