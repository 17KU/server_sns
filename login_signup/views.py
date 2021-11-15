from rest_framework.views import APIView
from .models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

class UserRegist(APIView):
    # APIView에 있는 post() method
    def post(self, request):
        # client로 부터 받은 id와 pw, name 저장
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')
        user_pw_encryted = make_password(user_pw)
        user_name = request.data.get('user_name')

        user = User.objects.filter(user_id = user_id).first()
        if user is not None:
            return JsonResponse({'code': '0001', 'msg': '동일한 아이디 존재'}, status=200)

        User.objects.create(user_id = user_id, user_pw = user_pw_encryted, user_name = user_name)

        return JsonResponse({'code': '0000', 'msg': '회원가입 성공'}, status=200)

class UserDupliCheck(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        user = User.objects.filter(user_id = user_id).first()
        if user is None:
            return JsonResponse({'code': '0000', 'msg': '사용 가능한 아이디'}, status = 200)
        else:
            return JsonResponse({'code': '0001', 'msg': '이미 존재하는 아이디'}, status = 200)

class UserLogin(APIView):
    # APIView에 있는 post() method
    def post(self, request):
        # client로 부터 받은 id와 pw 저장
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')

        user = User.objects.filter(user_id = user_id).first()

        if user is None:
            return JsonResponse({'code': '0001', 'msg': '로그인 실패, 아이디 틀림', 'user_id': None, 'user_name': None}, status=200)

        if check_password(user_pw, user.user_pw) :
            return JsonResponse({'code': '0000', 'msg': '로그인 성공', 'user_id': user.user_id, 'user_name': user.user_name}, status=200)
        else:
            return JsonResponse({'code': '0002', 'msg': '로그인 실패, 비밀번호 틀림', 'user_id': None, 'user_name': None}, status=200)


class UserNameChange(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')
        user_name = request.data.get('user_name')

        try :
            user = User.objects.get(user_id = user_id)
            if check_password(user_pw, user.user_pw):
                user.user_name = user_name
                user.save()
                return JsonResponse({'code': '0000', 'msg': user_name+'으로 이름 변경 완료'}, status = 200)
            else :
                return JsonResponse({'code': '0001', 'msg': '비밀번호가 틀렸습니다.'}, status=200)
        except User.DoesNotExist:
            pass

        return JsonResponse({'code': '0002', 'msg': '존재하지 않는 아이디입니다.'}, status=200)

class UserPwdChange(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')
        user_new_pw = request.data.get('user_new_pw')

        try:
            user = User.objects.get(user_id = user_id)
            if check_password(user_pw, user.user_pw):
                user_pw_encryted = make_password(user_new_pw)
                user.user_pw = user_pw_encryted
                user.save()
                return JsonResponse({'code': '0000', 'msg': user_new_pw+'비밀번호 변경 완료'}, status=200)
            else:
                return JsonResponse({'code': '0001', 'msg': '비밀번호가 틀렸습니다.'}, status=200)
        except User.DoesNotExist:
            pass

        return JsonResponse({'code': '0002', 'msg': '존재하지 않는 아이디입니다.'}, status=200)