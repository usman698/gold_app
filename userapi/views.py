from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from . serializer import UserSerializer
from django.core.mail import send_mail
from django.http import HttpResponse


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        ser = UserSerializer(user)

        # Add custom claims
        token['user_id'] = user.id
        # token['email'] = user.email
        token['current_user'] = ser.data
        # print(ser.data)
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
def mail(request):
    send_mail(
        'Django Email',
        'Auto generated email in django',
        'noreply@my700live.com',
        ['usmana8956@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Mail Sent Successfully.")