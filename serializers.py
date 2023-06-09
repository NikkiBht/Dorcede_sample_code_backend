from .models import PostSell, PostSellPictures, PostSellLikes, PostSellDeletes, PostSellReceivedInterest
from rest_framework import serializers
from account.models import Profile, Account
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework.fields import CurrentUserDefault
from rest_framework.reverse import reverse

# Serializers for API views

class ProfileSerializerForShowPost(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Profile model used in displaying posts, when we need a list of all posts. 
    This is to reduce the data size and only retrieve the profile data we need to show posts in a list.
    """
    first_name = serializers.CharField(source='user.first_name')
    
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'image')


class PostSerializerForGet(serializers.ModelSerializer):
    """
    Serializer for retrieving posts. This is used to show a list of all posts.
    """
    profile_obj = Profile.objects.all()
    poster = ProfileSerializerForShowPost(profile_obj)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['time'] = naturaltime(instance.time)
        return representation
    
    class Meta:
        model = PostSell
        fields = "__all__"


class PostSerializerForGetForMap(serializers.ModelSerializer):
    """
    Serializer for retrieving posts for map display. To reduce the data size on map.
    """
    class Meta:
        model = PostSell
        fields = ('id', 'latitude', 'longitude', 'price')


class PostSerializerForEachUser(serializers.ModelSerializer):
    """
    Serializer for retrieving posts for each user. This is to show on profile and anywhere we need post_type to be shown.
    """
    class Meta:
        model = PostSell
        fields = ('id', 'post_type', 'time')


class PostSerializerForPosting(serializers.ModelSerializer):
    """
    Serializer for posting new posts. This is to get a post request from user (user wants to make a new post)
    """
    class Meta:
        model = PostSell
        fields = ('id', 'poster', 'title', 'latitude', 'longitude', 'price', 'size', 'show_to_verified', 'description',
                  'flat_no', 'street_no', 'street', 'neighborhood', 'city', 'country', 'postal_code', 'condition', 'age', 'age_unit')


class PostPicturesSerializerForViewing(serializers.ModelSerializer):
    """
    Serializer for viewing post pictures. 
    This is to have each post and its picture in an API call. Used when user click on the post to see more detail.
    """
    class Meta:
        model = PostSellPictures
        fields = ('post', 'image')


class PostLikesSerializer(serializers.ModelSerializer):
    """
    Serializer for post likes. This is used to retrieve all the posts that were liked by a user.
    """
    post_detail = serializers.SerializerMethodField()
    
    def get_post_detail(self, obj):
        post = obj.post
        serializer = PostSerializerForGet(post, context=self.context)
        return serializer.data
    
    class Meta:
        model = PostSellLikes
        fields = ('post_detail', 'time')


class PostLikesSerializerForCreate(serializers.ModelSerializer):
    """
    Serializer for creating post likes. 
    This is used to allow user to create a like object.
    """
    class Meta:
        model = PostSellLikes
        fields = ('post', 'user')


class PostDeletesSerializer(serializers.ModelSerializer):
    """
    Serializer for post deletions. 
    This is used to call for all the posts that users removed from their feed.
    """
    post_detail = serializers.SerializerMethodField()
    
    def get_post_detail(self, obj):
        post = obj.post
        serializer = PostSerializerForGet(post, context=self.context)
        return serializer.data
    
    class Meta:
        model = PostSellDeletes
        fields = ('post_detail', 'time')


class PostDeletesSerializerForCreate(serializers.ModelSerializer):
    """
    Serializer for creating post deletions.
    This is used to allow user to hide posts from their feed.
    """
    class Meta:
        model = PostSellDeletes
        fields = ('post', 'user')


class ReceivedInterestSerializer(serializers.ModelSerializer):
    """
    Serializer for received interests on posts.
    This is used to show all the posts of one user that recieved an interest from another user.
    """
    buyer = ProfileSerializerForShowPost() 
    item_pictures = serializers.SerializerMethodField()
    item = PostSerializerForGet()
    
    def get_item_pictures(self, instance):
        item = instance.item
        pictures = PostSellPictures.objects.filter(post=item)
        serializer = PostPicturesSerializerForViewing(pictures, many=True, context=self.context)
        return serializer.data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['time'] = naturaltime(instance.time)
        return representation
    
    class Meta:
        model = PostSellReceivedInterest
        fields = ('id', 'buyer', 'item', 'time', 'item_pictures')
