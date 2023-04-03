from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from . serializer import UserSerializer
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from . models import Profile
import random


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
    

@api_view(["POST"])
def mail(request):
    if request.method == 'POST':
        try:
            User = get_user_model()
            id = request.data.get('id')
            print(id)
            email = request.data.get('email')
            print(email)
            user_obj = User.objects.get(id=id)
            profile_obj = Profile.objects.get(user=user_obj)
            number = random.randint(1000,9999)
            profile_obj.code = number
            profile_obj.save()
            send_mail(
                'Password Reset Email',
                number,
                'noreply@my700live.com',
                [email],
                fail_silently=False,
            )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)