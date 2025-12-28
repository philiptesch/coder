from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import offers, OfferDetails, Orders
from django.db.models import Min, Max, Avg, Sum, Count
from profile_app.api.serializers import UserDetailsSerializer





class DetailCreateSeralizer(serializers.ModelSerializer):

    delivery_time_in_days = serializers.IntegerField(source='delivery_time')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OfferDetails
        fields = ['id', 'revisions', 'title', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class DetailOfferSeralizer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='offer-details', lookup_field='pk')

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']



class OfferSeralizer(serializers.ModelSerializer):


    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField()
    details = DetailOfferSeralizer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user.profile', read_only=True) 

    def get_min_price(self, obj):
     return obj.details.aggregate(min_price=Min('price'))['min_price']
    
    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery_time=Min('delivery_time'))['min_delivery_time']

    def get_user(self, obj):
        return obj.user.id         


    class Meta:
        model = offers
        fields = ['id', 'user', 'title', 'image' ,'description', 'createad_at', 'uploaded_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferCreateSeralizer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    details = DetailCreateSeralizer(many=True)

    class Meta:
        model = offers
        fields = ['id', 'title', 'image', 'description', 'details']


    def create(self, validated_data):
 
        details_data = validated_data.pop('details', [])
        user = self.context['request'].user
        offer = offers.objects.create(**validated_data, user=user)
        print("OFFER CREATED:", offer)
    
        for detail_data in details_data:
            features = detail_data.get('features', [])

            for feature in features:
                if isinstance(feature, int):
                    raise serializers.ValidationError(
                        {"error": "Features dürfen keine Zahlen enthalten"}
                    )
            OfferDetails.objects.create(offer=offer, **detail_data)


        return offer



class OfferDetailSeralizerHyperlinked(serializers.HyperlinkedModelSerializer):
    

    url = serializers.HyperlinkedIdentityField(view_name='offer-retrieve-details', lookup_field='pk')
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']




class OfferDetailSeralizer(serializers.ModelSerializer):

    details = OfferDetailSeralizerHyperlinked(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()


    def get_user(self, obj):
        return obj.user.id
    

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']
    
    def get_min_delivery_time(self, obj):#
        return obj.details.aggregate(min_delivery_time=Min('delivery_time'))['min_delivery_time']
    class Meta:
        model = offers
        fields = ['id', 'user', 'title', 'image' ,'description', 'createad_at', 'uploaded_at', 'details', 'min_price', 'min_delivery_time',]

class OfferDetailRetrieveSeralizer(serializers.ModelSerializer):


    class Meta:
        model = OfferDetails
        fields = ['id', 'offer', 'revisions', 'title', 'delivery_time', 'price', 'features', 'offer_type']


class OfferDetailUpdateSeralizer(serializers.ModelSerializer):
    details = DetailCreateSeralizer(many=True)
    id = serializers.IntegerField(read_only=True)
    image = serializers.FileField(required=False, read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = offers 
        fields = ['id', 'image', 'description', 'title', 'details']

    def update(self, instance, validated_data):
        print("UPDATE CALLED")
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        existing_details = (OfferDetails.objects.filter(offer=instance))
        print("OFFER DETAILS EXISTING:", existing_details)

        details_data = validated_data.get('details', [])
        print("DETAILS DATA:", details_data)
        for i, detail_data in enumerate(details_data):                                                                               
            if i < len(existing_details):
                print("UPDATING DETAIL:",  existing_details[i].id)
                detail_instance = existing_details[i]
                detail_instance.revisions = detail_data.get('revisions', detail_instance.revisions)
                detail_instance.title = detail_data.get('title', detail_instance.title)
                detail_instance.delivery_time = detail_data.get('delivery_time', detail_instance.delivery_time)
                detail_instance.price = detail_data.get('price', detail_instance.price)
                detail_instance.features = detail_data.get('features', detail_instance.features)
                detail_instance.offer_type = detail_data.get('offer_type', detail_instance.offer_type)
                detail_instance.save()
            else:
                OfferDetails.objects.create(
                offer=instance,
                **detail_data
                )

                

        return instance