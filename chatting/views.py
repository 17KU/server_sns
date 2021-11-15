from rest_framework.views import APIView
from .models import User_Chat
from .models import Chat
from login_signup.models import User
from friends.models import user_friend
from django.http import JsonResponse


# Create your views here.

class ChatListSelect(APIView):
    # APIView에 있는 post() method
    def post(self, request):
        # client로 부터 받은 user_id 저장
        user_id = request.data.get('user_id')

        # 해당하는 유저의 채팅방 목록을 저장할 리스트
        result_list = []

        # 정방향
        # User_Chat 테이블에서 해당하는 유저의 모든 chat_index를 가지고 옴
        uc_chat_index_list = []
        user_chat_list = User_Chat.objects.filter(uc_user_id=user_id).all()
        for user_chat in user_chat_list:
            uc_chat_index_list.append(user_chat.uc_chat_index)

        # 정방향 추가
        for uc_chat_index in uc_chat_index_list:
            my_chat = Chat.objects.filter(chat_index=uc_chat_index.chat_index).first()
            my_title = User.objects.filter(user_id=my_chat.chat_other_id).first().user_name
            result_list.append(dict(chat_index=my_chat.chat_index,
                                  chat_title=my_title,
                                  chat_other_id=my_chat.chat_other_id,
                                  code='0002',
                                  msg='채팅 있음. 해당 유저가 추가한 채팅방'
                                  ))

        # 역방향
        # Chat 테이블에서 chat_other_id가 자기 자신이면 모든 Chat 객체를 가져옴
        chat_index_list = []
        chat_list = Chat.objects.filter(chat_other_id=user_id).all()
        for chat in chat_list :
            chat_index_list.append(chat.chat_index)

        # 역방향 추가
        for chat_index in chat_index_list :
            my_user_chat = User_Chat.objects.filter(uc_chat_index = chat_index).first()
            my_uc_title = User.objects.filter(user_id = my_user_chat.uc_user_id.user_id).first().user_name
            result_list.append(dict(chat_index = my_user_chat.uc_chat_index.chat_index,
                                  chat_title = my_uc_title,
                                  chat_other_id = my_user_chat.uc_user_id.user_id,
                                  code='0003',
                                  msg='채팅 있음. 다른 유저가 추가한 채팅방'
                                  ))


        if len(result_list) > 0:
            return JsonResponse(result_list, safe=False)
        else:
            result_list.append(dict(chat_index=None,
                                  chat_title=None,
                                  chat_other_id=None,
                                  code='0001',
                                  msg='채팅 없음'
                                  ))
            return JsonResponse(result_list, safe=False)


class ChatListInsert(APIView):
    # APIView에 있는 post() method
    def post(self, request):
        # client로 부터 받은 user_id, friend_id 저장
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')

        friend = user_friend.objects.filter(uf_user_id = user_id, uf_friend_id = friend_id).first()

        #친구 관계일때
        if friend is not None:

            user_instance = User.objects.filter(user_id=user_id).first()
            my_chat_list = []

            # 리스트에 정방향 채팅 인덱스 추가
            uc_list = User_Chat.objects.filter(uc_user_id = user_instance).all()
            for my_uc in uc_list :
                my_chat_list.append(my_uc.uc_chat_index.chat_index)

            # 리스트에 역방향 채팅 인덱스 추가
            c_list = Chat.objects.filter(chat_other_id = user_instance.user_id).all()
            for my_c in c_list :
                my_chat_list.append(my_c.chat_index)

            # 채팅방이 하나 이상 존재할때
            if len(my_chat_list) != 0 :
                for my_chat_index in my_chat_list:
                    chat = Chat.objects.filter(chat_index = my_chat_index).first()
                    user_chat = User_Chat.objects.filter(uc_chat_index = my_chat_index).first()
                    #이미 존재하는 채팅방일때
                    if ((chat is not None) and (chat.chat_other_id == friend_id)):
                        return JsonResponse({'chat_index': chat.chat_index, 'chat_title': chat.chat_title, 'chat_other_id': chat.chat_other_id, 'code': '0002', 'msg': '내가 이미 만든 채팅방 입니다.'}, status=200)
                    if ((user_chat is not None) and (user_chat.uc_user_id.user_id == friend_id)):
                        name = User.objects.filter(user_id = friend_id).first().user_name
                        return JsonResponse(
                            {'chat_index': user_chat.uc_chat_index.chat_index, 'chat_title': name, 'chat_other_id': friend_id, 'code': '0003', 'msg': '친구가 이미 만든 채팅방 입니다.'}, status=200)

                #존재하지 않는 채팅방일때
                friend_name = User.objects.filter(user_id=friend_id).first().user_name
                #user_instance = User.objects.filter(user_id = user_id).first()
                new_chat = Chat.objects.create(chat_title=friend_name, chat_other_id=friend_id)
                User_Chat.objects.create(uc_chat_index=new_chat, uc_user_id=user_instance)
                print("기존 채팅방 개수 : ", len(my_chat_list))
                return JsonResponse({'chat_index': new_chat.chat_index, 'chat_title': new_chat.chat_title, 'chat_other_id': new_chat.chat_other_id, 'code': '0004', 'msg': '채팅방 새로 개설'}, status=200)
            #채팅방이 하나도 없을때
            else:
                friend_name = User.objects.filter(user_id=friend_id).first().user_name
                #user_instance = User.objects.filter(user_id=user_id).first()
                new_chat = Chat.objects.create(chat_title=friend_name, chat_other_id=friend_id)
                User_Chat.objects.create(uc_chat_index=new_chat, uc_user_id=user_instance)
                return JsonResponse({'chat_index': new_chat.chat_index, 'chat_title': new_chat.chat_title, 'chat_other_id': new_chat.chat_other_id, 'code': '0005', 'msg': '채팅방 새로 개설 (첫번째 채팅방)'}, status=200)

        #친구 관계 아닐때
        else:
            return JsonResponse({'chat_index': None, 'chat_title': None, 'chat_other_id': None, 'code': '0001', 'msg': '서로 친구 관계가 아닙니다.'}, status=200)



class ChatListDelete(APIView):
    def post(self, request):
        chat_index = request.data.get('chat_index')
        user_id = request.data.get('user_id')

        try:
            user_chat = User_Chat.objects.get(uc_chat_index=chat_index)
            chat = Chat.objects.get(chat_index=chat_index)

            # 존재하는 채팅방인지 체크
            if (user_chat is not None) and (chat is not None):
                # 권한 체크
                if (user_chat.uc_user_id.user_id == user_id) or (chat.chat_other_id == user_id):
                    user_chat.delete()
                    chat.delete()
                    return JsonResponse({"code": "0000", "msg": "채팅방을 삭제했습니다."}, status=200)
                else:
                    return JsonResponse({"code": "0001", "msg": "채팅방을 삭제할 권한이 없습니다."}, status=200)

        except User_Chat.DoesNotExist:
            pass
        except Chat.DoesNotExist:
            pass

        return JsonResponse({"code": "0002", "msg": "삭제할 채팅방이 존재하지 않습니다."}, status=200)
