from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User


class DetailProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)


 
    
    class Meta:
        model = Profile
        fields = ['user', 'username','first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'created_at',
        'type', 'email']