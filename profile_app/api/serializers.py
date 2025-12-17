from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User


class DetailProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', required=False)
    type = serializers.CharField(source='user.type', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'created_at',
                  'type', 'email']

    def get_user(self, obj):
        return obj.user.id

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get('file'):
            data['file'] = ""
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', {})
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()
            instance.email = email
            User.objects.filter(id=instance.user.id).update(email=email)

        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.location = validated_data.get('location', instance.location)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.working_hours = validated_data.get(
            'working_hours', instance.working_hours)
        instance.description = validated_data.get(
            'description', instance.description)

        instance.save()
        return instance
