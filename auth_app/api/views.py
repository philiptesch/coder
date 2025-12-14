from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from auth_app.api.seralizers import RegistrationSerializer, LoginSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'type': user.type,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
   
    def post(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.validated_data['user']
          token, created = Token.objects.get_or_create(user=user)
          return Response({
              'user_id': user.id,
              'username': user.username,
              'email': user.email,
              'token': token.key
          })