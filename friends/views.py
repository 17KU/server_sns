from MySQLdb import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import user_friend
from login_signup.models import User
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chatting.models import User_Chat
from chatting.models import Chat

# Create your views here.

class AddFriend(APIView):
    def post(self, request):

        user_id = request.data.get('user_id')
        add_friend_id = request.data.get('add_friend_id')


        # 유저 아이디가 올바른지

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            return JsonResponse({'code':'0001', 'msg':'아이디가 존재하지 않습니다'}, status=200)

        # 친구 추가할 ID가 User 테이블에 존재하는지
        #try:
        #   friend = User.objects.filter(user_id=add_friend_id).first()
        #except friend.DoesNotExist:
        #    return JsonResponse({'code':'0001','msg':'상대방이 존재하지 않습니다'}, status=200)

        # 친구 추가할 ID가 User 테이블에 존재하는지
        friend = User.objects.filter(user_id=add_friend_id).first()
        if friend is None:
            return JsonResponse({'code':'0001','msg':'상대방이 존재하지 않습니다'}, status=200)

        # 친구 추가 하기

        # 친구 추가 아이디가 본인 아이디 와 같으면
        if user_id == add_friend_id:
            return JsonResponse({'code':'0002', 'msg':'본인을 추가할 수 없습니다'}, status=200)

        #criterion1 = Q(uf_user_id=user_id)
        #criterion2 = Q(uf_friend_id=add_friend_id)

        # 원래 친구가 아니면
        friend = user_friend.objects.filter(uf_user_id=user_id,uf_friend_id=add_friend_id).first()

        if friend is None:
            user_friend.objects.create(uf_user_id=user, uf_friend_id=add_friend_id)
            return JsonResponse({'code': '0000', 'mgs': 'success', 'user_id': user_id, 'add_friend_id': add_friend_id},
                                status=200)
        else:
            return JsonResponse({'code':'0003', 'msg':'이미 친구입니다'},status=200)

class DeleteFriend(APIView):
    def post(self, request):

        user_id = request.data.get('user_id')
        delete_friend_id = request.data.get('delete_friend_id')

        # 유저 아이디가 올바른지

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            return JsonResponse({'code': '0001', 'msg': '아이디가 존재하지 않습니다'}, status=200)

        # 친구 추가할 ID가 User 테이블에 존재하는지
        friend = User.objects.filter(user_id=delete_friend_id).first()
        if friend is None:
            return JsonResponse({'code': '0001', 'msg': '상대방이 존재하지 않습니다'}, status=200)

        #친구 삭제하기

        # 친구 삭제 아이디가 본인 아이디 와 같으면
        if user_id == delete_friend_id:
            return JsonResponse({'code': '0002', 'msg': '본인을 삭제할 수 없습니다'}, status=200)

        # 원래 친구가 아니면
        friend = user_friend.objects.filter(uf_user_id=user_id, uf_friend_id=delete_friend_id).first()

        if friend is None:
            return JsonResponse({'code': '0003', 'msg': '친구가 아닙니다'}, status=200)
        else:
            friend.delete()
            return JsonResponse({'code': '0000', 'msg': 'success', 'user_id': user_id, 'delete_friend_id': delete_friend_id},
                                status=200)


        return JsonResponse()



class ShowFriend(APIView):

    def post(self, request):

        user_id = request.data.get('user_id')

        # 유저 아이디가 올바른지

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            return JsonResponse({'code': '0001', 'msg': '유저 없음'}, status=200)

        # 유저 아이디에 해당하는 친구 목록
        friend = user_friend.objects.filter(uf_user_id=user_id).all()

        friend_list = []

        #즐겨찾기 된 친구인지까지 같이 보냄
        for index in friend:
            friend_name = User.objects.filter(user_id=index.uf_friend_id).first().user_name
            friend_list.append(dict(uf_friend_name=friend_name,uf_friend_id= index.uf_friend_id, uf_favorite_state=index.uf_favorite))


        if len(friend_list) >0:
            return JsonResponse(friend_list, safe=False)

        else:
            return JsonResponse({'code': '0002', 'msg': '친구 없음'}, status=200)




class AddFavorite(APIView):

    def post(self, request):

        user_id = request.data.get('user_id')
        favorite_add = request.data.get('favorite_add')


        # 유저 아이디가 올바른지
        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            return JsonResponse({'code': '0001', 'msg': '아이디가 존재하지 않습니다'}, status=200)

        # 즐찾할 아이디가 올바른지
        friend = User.objects.filter(user_id=favorite_add).first()
        if friend is None:
            return JsonResponse({'code': '0001', 'msg': '유저 없음'}, status=200)

        # 즐겨찾기
        favorite = user_friend.objects.filter(uf_user_id=user_id,uf_friend_id=favorite_add).first()

        # 즐겨찾기 해제
        if favorite.uf_favorite is True :
            favorite.uf_favorite = False
            favorite.save()
            return JsonResponse({'code':'0002', 'msg': '즐겨찾기 해제'}, status=200)

        # 즐겨찾기 추가
        elif favorite.uf_favorite is False :
            favorite.uf_favorite = True
            favorite.save()
            return JsonResponse({'code': '0003', 'msg': '즐겨찾기 추가가'}, status=200)





class findChat(APIView):
    # APIView에 있는 post() method
    def post(self, request):
        # client로 부터 받은 user_id, friend_id 저장
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')

        friend = user_friend.objects.filter(uf_user_id=user_id, uf_friend_id=friend_id).first()

        # 친구 관계일때
        if friend is not None:

            user_instance = User.objects.filter(user_id=user_id).first()
            my_chat_list = []

            # 리스트에 정방향 채팅 인덱스 추가
            uc_list = User_Chat.objects.filter(uc_user_id=user_instance).all()
            for my_uc in uc_list:
                my_chat_list.append(my_uc.uc_chat_index.chat_index)

            # 리스트에 역방향 채팅 인덱스 추가
            c_list = Chat.objects.filter(chat_other_id=user_instance.user_id).all()
            for my_c in c_list:
                my_chat_list.append(my_c.chat_index)

            # 채팅방이 하나 이상 존재할때
            if len(my_chat_list) != 0:
                for my_chat_index in my_chat_list:
                    chat = Chat.objects.filter(chat_index=my_chat_index).first()
                    user_chat = User_Chat.objects.filter(uc_chat_index=my_chat_index).first()
                    # 이미 존재하는 채팅방일때
                    if ((chat is not None) and (chat.chat_other_id == friend_id)):
                        return JsonResponse({'chat_index': chat.chat_index, 'chat_title': chat.chat_title,
                                             'chat_other_id': chat.chat_other_id, 'code': '0002',
                                             'msg': '내가 이미 만든 채팅방 입니다.'}, status=200)
                    if ((user_chat is not None) and (user_chat.uc_user_id.user_id == friend_id)):
                        name = User.objects.filter(user_id=friend_id).first().user_name
                        return JsonResponse(
                            {'chat_index': user_chat.uc_chat_index.chat_index, 'chat_title': name,
                             'chat_other_id': friend_id, 'code': '0003', 'msg': '친구가 이미 만든 채팅방 입니다.'}, status=200)

                # 존재하지 않는 채팅방일때
                friend_name = User.objects.filter(user_id=friend_id).first().user_name
                # user_instance = User.objects.filter(user_id = user_id).first()
                new_chat = Chat.objects.create(chat_title=friend_name, chat_other_id=friend_id)
                User_Chat.objects.create(uc_chat_index=new_chat, uc_user_id=user_instance)
                print("기존 채팅방 개수 : ", len(my_chat_list))
                return JsonResponse({'chat_index': new_chat.chat_index, 'chat_title': new_chat.chat_title,
                                     'chat_other_id': new_chat.chat_other_id, 'code': '0004', 'msg': '채팅방 새로 개설'},
                                    status=200)
            # 채팅방이 하나도 없을때
            else:
                friend_name = User.objects.filter(user_id=friend_id).first().user_name
                # user_instance = User.objects.filter(user_id=user_id).first()
                new_chat = Chat.objects.create(chat_title=friend_name, chat_other_id=friend_id)
                User_Chat.objects.create(uc_chat_index=new_chat, uc_user_id=user_instance)
                return JsonResponse({'chat_index': new_chat.chat_index, 'chat_title': new_chat.chat_title,
                                     'chat_other_id': new_chat.chat_other_id, 'code': '0005',
                                     'msg': '채팅방 새로 개설 (첫번째 채팅방)'}, status=200)

        # 친구 관계 아닐때
        else:
            return JsonResponse({'chat_index': None, 'chat_title': None, 'chat_other_id': None, 'code': '0001',
                                 'msg': '서로 친구 관계가 아닙니다.'}, status=200)
