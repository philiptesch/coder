from rest_framework import serializers
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import Offers, OfferDetails, Orders, Review
from django.db.models import Min, Max, Avg, Sum, Count
from profile_app.api.serializers import UserDetailsSerializer





class DetailCreateSeralizer(serializers.ModelSerializer):
    """
    Serializer for creating offer detail entries.

    Purpose:
        Used when creating or updating an offer with multiple detail options.

    Field mapping:
        delivery_time_in_days maps to delivery_time in the model.
    """

    delivery_time_in_days = serializers.IntegerField(source='delivery_time')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OfferDetails
        fields = ['id', 'revisions', 'title', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class DetailOfferSeralizer(serializers.HyperlinkedModelSerializer):
    """
    Lightweight serializer for offer details.

    Purpose:
        Used to expose only the ID and URL of offer details
        when listing offers.
    """

    url = serializers.HyperlinkedIdentityField(view_name='offer-details', lookup_field='pk')

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']



class OfferSeralizer(serializers.ModelSerializer):
    """
    Serializer for listing offers.

    Includes:
        - Basic offer information
        - Related offer details (URLs only)
        - Minimum price and delivery time (aggregated)
        - Business user details

    Read-only:
        All computed fields are derived from related data.
    """

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
        model = Offers
        fields = ['id', 'user', 'title', 'image' ,'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferCreateSeralizer(serializers.ModelSerializer):
    """
    Serializer for creating a new offer.

    Behavior:
        - Requires at least three offer detail entries.
        - Automatically assigns the authenticated user as owner.

    Validation:
        - Ensures features do not contain numeric values.
    """

    id = serializers.IntegerField(read_only=True)
    details = DetailCreateSeralizer(many=True)

    class Meta:
        model = Offers
        fields = ['id', 'title', 'image', 'description', 'details']


    def create(self, validated_data):
 
        details_data = validated_data.pop('details', [])
        user = self.context['request'].user
        if len(details_data) < 3:
             raise serializers.ValidationError(
                        {"error": "a Offer must have at least three details  "}
             )
        offer = Offers.objects.create(**validated_data, user=user)

        for detail_data in details_data:
            features = detail_data.get('features', [])

            for feature in features:
                if isinstance(feature, int):
                    raise serializers.ValidationError(
                        {"error": "features must not contain numbers"}
                    )
            OfferDetails.objects.create(offer=offer, **detail_data)


        return offer



class OfferDetailSeralizerHyperlinked(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for offer details.

    Purpose:
        Used to reference individual offer detail endpoints
        from an offer detail response.
    """

    url = serializers.HyperlinkedIdentityField(view_name='offer-retrieve-details', lookup_field='pk')
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']




class OfferDetailSeralizer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single offer with full details.

    Includes:
        - All related offer detail links
        - Aggregated minimum price
        - Aggregated minimum delivery time
        - Owner user ID
    """

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
        model = Offers
        fields = ['id', 'user', 'title', 'image' ,'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time',]

class OfferDetailRetrieveSeralizer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single offer detail.

    Purpose:
        Used when accessing a specific offer detail directly.
    """
    delivery_time_in_days = serializers.IntegerField(source='delivery_time')
    class Meta:
        model = OfferDetails
        fields = ['id', 'offer', 'revisions', 'title', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailUpdateSeralizer(serializers.ModelSerializer):
    """
    Serializer for updating an existing offer and its details.

    Behavior:
        - Updates the offer title.
        - Updates existing detail entries or creates new ones.
        - Offer type is mandatory for each detail.

    Restrictions:
        Image and description cannot be modified here.
    """
    details = DetailCreateSeralizer(many=True)
    id = serializers.IntegerField(read_only=True)
    image = serializers.FileField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = Offers
        fields = ['id', 'image', 'description', 'title', 'details']


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        existing_details = list(OfferDetails.objects.filter(offer=instance))
        details_data = validated_data.get('details', [])
        for i, detail_data in enumerate(details_data):
            offer_type = detail_data.get('offer_type')
            if not offer_type:
                raise serializers.ValidationError("Offer type is required.")
            if i < len(existing_details):
                detail_instance = existing_details[i]
                detail_instance.title = detail_data.get('title', detail_instance.title)
                detail_instance.revisions = detail_data.get('revisions', detail_instance.revisions)
                detail_instance.delivery_time = detail_data.get('delivery_time_in_days', detail_instance.delivery_time)
                detail_instance.price = detail_data.get('price', detail_instance.price)
                detail_instance.features = detail_data.get('features', detail_instance.features)
                detail_instance.offer_type = offer_type
                detail_instance.save()
            else:
                OfferDetails.objects.create(offer=instance,title=detail_data.get('title'),revisions=detail_data.get('revisions', 0),delivery_time=detail_data.get('delivery_time_in_days', 0),price=detail_data.get('price', 0),features=detail_data.get('features', []),offer_type=offer_type)

        return instance


    



class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing orders.

    Behavior:
        - Accepts offer_detail_id as input.
        - Automatically assigns customer and business users.
        - Exposes read-only fields from related offer detail.
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Orders
        fields = [
            'id', 'customer_user', 'business_user',
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type', 'status',
            'created_at', 'updated_at', 'offer_detail_id'
        ]
        read_only_fields = ['customer_user', 'business_user', 'status', 'created_at', 'uploaded_at']

    def create(self, validated_data):

        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetails.objects.get(id=offer_detail_id)
        user = self.context['request'].user

        order = Orders.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            **validated_data
        )
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating a single order.

    Update rules:
        - Only the 'status' field can be updated.
        - Any other field update is rejected.
    """
    
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Orders
        fields = [
            'id', 'customer_user', 'business_user',
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user',
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
            'created_at', 'updated_at'
        ]

    def validate(self, data):
        allowed_fields = {'status'}
        for field in data:
            if field not in allowed_fields:
                raise serializers.ValidationError(
                    {field: f"You cannot update the field '{field}'."}
                )
        return data

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)


        if 'status' in validated_data:
            instance.status = validated_data['status']
        else:
            raise serializers.ValidationError({"status": "This field is required for update."})
        instance.save()
        return instance

class ReviewListSeralizer(serializers.ModelSerializer):
    """
    Serializer for listing and creating reviews.

    Field mapping:
        rating maps to the 'rate' field in the model.

    Restrictions:
        Reviewer is always read-only and set automatically.
    """

    id = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(source='rate')


    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer',
            'rating', 'description', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'reviewer',
            'created_at',
            'updated_at']
    


class ReviewDetailSeralizer(serializers.ModelSerializer):
    """
    Serializer for updating or retrieving a single review.

    Update behavior:
        - Allows updating rating and description only.
        - Reviewer and business user cannot be changed.
    """

    id = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(source='rate')


    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer',
            'rating', 'description', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'reviewer', 'business_user'
            'created_at', 'updated_at']
        
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.rate = validated_data.get('rate', instance.rate)
        

        instance.save()
        return instance


class BaseSerializer(serializers.Serializer):
    """
    Serializer providing aggregated platform statistics.

    Returns:
        - Total review count
        - Average review rating
        - Number of business profiles
        - Total number of offers
    """
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        return Review.objects.count()  

    def get_average_rating(self, obj):
        rating_average = Review.objects.aggregate(avg=Avg('rate'))['avg'] or 0
        return round(rating_average, 1)

    def get_business_profile_count(self, obj):
       business_user =  User.objects.filter(type='business')
       return business_user.count()

    def get_offer_count(self, obj):
        return Offers.objects.count()


