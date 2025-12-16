from rest_framework import serializers
from auth_app.models import User
from django.contrib.auth import authenticate
from profile_app.models import Profile




class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['id', 'username', 'email', 'type', 'created_at']
     




class RegistrationSerializer(serializers.ModelSerializer):
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
            user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            type=validated_data['type']
            )
            user.set_password(validated_data['password']) 
            user.save()
            Profile.objects.create(user=user)
            return user
    

class LoginSerializer(serializers.Serializer):
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