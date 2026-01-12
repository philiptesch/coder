from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User


class DetailProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user profile information.

    Purpose:
        - Exposes all profile fields including related user information.
        - Handles updates to both the Profile and the related User object (e.g., email).

    Fields:
        - user: User ID
        - username: Username of the user
        - email: User's email (optional for update)
        - type: User type (customer or business)
        - created_at: Account creation timestamp
        - first_name, last_name: Profile names
        - file: Profile picture/file
        - location: Profile location
        - tel: Contact number
        - description: Profile description
        - working_hours: Profile working hours

    Behavior:
        - `get_user`: Returns the ID of the related User.
        - `to_representation`: Ensures 'file' field is never None (empty string if missing).
        - `update`: Allows updating both Profile fields and the related User's email.
    """

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
    
class BusinessProfileSeralizer(serializers.ModelSerializer):
    """
    Serializer for business user profiles.

    Purpose:
        - Exposes profile fields relevant for business users.
        - Read-only user fields: username, type.
        - Handles empty file field by returning an empty string if not set.

    Fields:
        - user: User ID
        - username: Username of the user
        - type: User type (business)
        - first_name, last_name: Profile names
        - file: Profile picture/file
        - location: Profile location
        - tel: Contact number
        - description: Profile description
        - working_hours: Business working hours
    """

    user = serializers.SerializerMethodField()
    type = serializers.CharField(source='user.type', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_user(self, obj):
        return obj.user.id

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get('file'):
            data['file'] = ""
        return data


class CustomerProfileSeralizer(serializers.ModelSerializer):
    """
    Serializer for customer user profiles.

    Purpose:
        - Exposes profile fields relevant for customer users.
        - Read-only user fields: username, type.
        - Handles empty file field by returning an empty string if not set.

    Fields:
        - user: User ID
        - username: Username of the user
        - type: User type (customer)
        - first_name, last_name: Profile names
        - file: Profile picture/file
    """

    user = serializers.SerializerMethodField()
    type = serializers.CharField(source='user.type', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'type']

    def get_user(self, obj):
        return obj.user.id

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get('file'):
            data['file'] = ""
        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for basic user details linked to a profile.

    Purpose:
        - Provides minimal user information for nested serialization.
        - Typically used inside other serializers (e.g., OfferSeralizer) to show user info.

    Fields:
        - first_name: User first name
        - last_name: User last name
        - username: Username
    """

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','username', ]

    


