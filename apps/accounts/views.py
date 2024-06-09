from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import CustomUser
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UsersModelView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RegisterUserViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            # Отправка письма с подтверждением
            send_confirmation_email(user)
            return Response(
                {'user': serializer.data,
                 'token': {'refresh': str(refresh), 'access': str(refresh.access_token),
                           }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core.mail import send_mail


def send_confirmation_email(user):
    subject = 'Подтверждение регистрации'
    message = 'Добро пожаловать! Для завершения регистрации перейдите по ссылке: <ваша_ссылка>'
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, email=serializer.data.get('email')
        )
        request.session['remember_me'] = serializer.data.get(
            'remember_me', False
        )
        refresh = RefreshToken.for_user(user)

        return Response(
            {'user': serializer.data,
             'token': {'refresh': str(refresh), 'access': str(refresh.access_token),
                       }}, status=status.HTTP_200_OK)


class ExternalAPIDataView(APIView):
    def get(self, request, *args, **kwargs):
        url = "https://rickandmortyapi.com/api/character"
        params = request.query_params  # Получаем параметры запроса
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Проверка наличия ошибок HTTP
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as http_err:
            return Response({'error': f'HTTP error occurred: {http_err}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': f'Other error occurred: {err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
