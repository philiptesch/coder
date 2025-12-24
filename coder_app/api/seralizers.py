from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import offers, Feature, OfferDetails, Orders


class DetailOfferSeralizer(serializers.HyperlinkedModelSerializer):

    id = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='offer-details', lookup_field='pk')


    def get_user(self, obj):
        return obj.user.id

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']



class OfferSeralizer(serializers.ModelSerializer):


    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField()
    details = DetailOfferSeralizer(many=True, source='offerdetails_set', read_only=True)

    def get_user(self, obj):
        return obj.user.id


    class Meta:
        model = offers
        fields = ['id', 'user', 'title', 'image' 'description', 'createad_at', 'uploaded_at', 'details']

    def get_user(self, obj):
        return obj.user.id