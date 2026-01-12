from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from auth_app.api.seralizers import RegistrationSerializer, LoginSerializer

class RegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Purpose:
        - Allows new users to register an account.
        - Uses the `RegistrationSerializer` for input validation.
        - Automatically generates an authentication token for the new user.

    Behavior:
        - Validates the request data using the serializer.
        - Saves the user to the database.
        - Creates or retrieves a token for the user.
        - Returns user details along with the token in the response.

    Response Fields:
        - user_id: ID of the newly created user
        - username: Username
        - email: User email
        - type: User type (customer or business)
        - token: Authentication token for the user

    HTTP Methods:
        - POST: Create a new user and return their info with token.
    """
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
    """
    API endpoint for user login.

    Purpose:
        - Authenticates an existing user using username and password.
        - Uses the `LoginSerializer` for validation.
        - Returns an authentication token upon successful login.

    Behavior:
        - Validates the request data using the serializer.
        - Authenticates the user.
        - Creates or retrieves a token for the user.
        - Returns user details along with the token in the response.

    Response Fields:
        - user_id: ID of the authenticated user
        - username: Username
        - email: User email
        - token: Authentication token for the user

    HTTP Methods:
        - POST: Authenticate the user and return their token.
    """
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