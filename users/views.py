import time

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User
from users.serializers import UserSerializer
from users.services import generate_otp, generate_referral_link

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Создание пользовтеля"""
        phone = self.request.data.get('phone')
        password = self.request.data.get('password')
        otp = generate_otp()

        new_user = User.objects.create_user(
            phone=phone,
            password=password
        )
        new_user.otp = otp
        new_user.save()
        time.sleep(2)
        return Response({"Ваш код активации": new_user.otp})
    
    @action(detail=False, methods=['post'])
    def otp(self, request):
        """Ввод кода активации"""
        current_user = User.objects.get(phone=request.data.get('phone'))
        referral_link = generate_referral_link()
        if request.data.get('otp') == current_user.otp:
            current_user.is_active = True
            current_user.first_login = True
            current_user.referral_link = referral_link
            current_user.save()
        return Response({"Ваш номер активирован. Ваша реферальная ссылка": current_user.referral_link})
    
    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def profile(self, request, pk=None):
        """Профиль пользователя со списком пользователей, активировавших ссылку текущего пользователя"""
        if request.method == 'POST':
            user = self.request.user
            referral_link = self.request.data.get('referral_link')
            referral_link_list = User.objects.filter(referral_link=referral_link).values_list('referral_link', flat=True)
            if user.activated_link in referral_link_list:
                return Response({"phone": str(user.phone), 
                                 "referral_link": user.referral_link,
                                 "activated_link": user.activated_link})
            elif user.referral_link== referral_link:
                return Response({"Нельзя вводить свою реферальную ссылку"})
            elif referral_link in referral_link_list:
                user.activated_link = referral_link
                user.save()
                return Response({"Ссылка активирована"})
            else:
                return Response({"Недействительная реферальная ссылка"})
        elif request.method == 'GET':
            user = self.request.user
            invited_users = User.objects.filter(activated_link=user.referral_link).values_list('phone', flat=True)
            return Response({"phone": str(user.phone), 
                             "referral_link": user.referral_link,
                             "invited_users": invited_users})

        