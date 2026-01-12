from rest_framework import serializers
from auth_app.models import User
from django.contrib.auth import authenticate
from profile_app.models import Profile




class UserProfileSerializer(serializers.ModelSerializer):
        """
    Serializer for user profile information.

    Purpose:
        - Used to expose basic user information.
        - Read-only serializer for displaying user data.

    Fields:
        - id: User ID
        - username: Username of the user
        - email: Email address
        - type: Type of user (customer or business)
        - created_at: Account creation timestamp
    """
class Meta:
    model = User
    fields = ['id', 'username', 'email', 'type', 'created_at']
     




class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Purpose:
        - Handles creating a new user account.
        - Validates email uniqueness.
        - Ensures passwords match.
        - Assigns user type (customer or business).
        - Automatically creates a related Profile object.

    Fields:
        - username: Desired username
        - email: User email address
        - password: Account password (write-only)
        - repeated_password: Password confirmation (write-only)
        - user_id: Read-only ID of the newly created user
        - type: Type of user ('customer' or 'business', write-only)

    Validation:
        - validate_email: Ensures email is unique.
        - validate_type: Ensures valid user type is selected.
        - validate: Ensures password and repeated_password match.

    Behavior:
        - On creation, splits username into first_name and last_name for Profile.
        - Sets the password securely using set_password.
    """

    user_id = serializers.IntegerField(read_only=True) 
    repeated_password = serializers.CharField(write_only=True) 
    type = serializers.ChoiceField(choices=User.UserType.choices,  write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'user_id', 'type']

    def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email is already in use.")
            return value
    
    def validate_type(self, value):
            if not value:
                    raise serializers.ValidationError("User type is required.")
            if value not in dict(User.UserType.choices).keys():
                raise serializers.ValidationError("Invalid user type.")
            return value
         
        
    def validate(self, data):
            if data['password'] != data['repeated_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match'})
            return data
        
    def create(self, validated_data):
            usernameForProfile = validated_data['username'],
            names = usernameForProfile[0].split(' ')
            firstname = names[0]
            if len(names) >= 2:
                 lastname = names[1]
            else: 
                 lastname = ""


            user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            type=validated_data['type']
            )
            user.set_password(validated_data['password']) 
            user.save()
            Profile.objects.create(user=user, first_name=firstname, last_name=lastname  )
            
            return user
    

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Purpose:
        - Authenticates a user using username and password.
        - Returns the authenticated user object if credentials are valid.

    Fields:
        - username: Username of the user
        - password: Password (write-only)

    Validation:
        - Checks that the username exists.
        - Authenticates credentials using Django's `authenticate`.
        - Raises ValidationError if credentials are invalid.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data