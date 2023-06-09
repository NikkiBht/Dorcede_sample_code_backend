from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import PostSell, PostSellPictures, PostSellLikes, PostSellDeletes, PostSellReceivedInterest
from .serializers import (
    PostSerializerForGet, PostSerializerForPosting, PostPicturesSerilizerforViewing,
    PostSerializerForGetForMap, PostSerializerForEachUser, PostLikesSerializer,
    PostLikesSerializerForCreate, RecievedInterestSerializer, PostDeletesSerializer,
    PostDeletesSerializerForCreate
)
from account.models import Profile
from account.serializers import AccountSerializer

# API view to search and retrieve post sells for viewing
class SearchPostSellsForViewing(APIView):
    """
    API view to search and retrieve post sells for viewing.
    """

    def get(self, request, format=None):
        """
        Retrieve post sells based on search query and filters.
        """
        query = request.GET.get('q')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        # Retrieve all post sells
        Posts_Sell_queryset = PostSell.objects.all().order_by('-time')

        # Apply search query filter
        if query:
            Posts_Sell_queryset = Posts_Sell_queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(size__icontains=query)
            )

        # Apply price range filters
        if price_min and price_max:
            Posts_Sell_queryset = Posts_Sell_queryset.filter(price__range=(price_min, price_max))
        else:
            if price_min:
                Posts_Sell_queryset = Posts_Sell_queryset.filter(price__gte=price_min)
            if price_max:
                Posts_Sell_queryset = Posts_Sell_queryset.filter(price__lte=price_max)

        # Exclude deleted posts if user is authenticated
        if request.user.is_authenticated:
            deleted_posts = PostSellDeletes.objects.filter(user=request.user).values_list('post', flat=True)
            Posts_Sell_queryset = Posts_Sell_queryset.exclude(id__in=deleted_posts)

        if Posts_Sell_queryset:
            # Serialize and return the post sells
            Posts_Sell_obj_serializer = PostSerializerForGet(Posts_Sell_queryset, many=True, context={'request': request})
            return Response(Posts_Sell_obj_serializer.data, status=200)
        else:
            return Response("No posts found", status=200)


# API view to search and retrieve post sells for viewing on map
class SearchPostSellsForViewingOnMap(APIView):
    """
    API view to search and retrieve post sells for viewing on map.
    """

    def get(self, request, format=None):
        """
        Retrieve post sells based on search query and filters for map view.
        """
        query = request.GET.get('q')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        # Retrieve all post sells
        Posts_Sell_queryset = PostSell.objects.all().order_by('-time')

        # Apply search query filter
        if query:
            Posts_Sell_queryset = Posts_Sell_queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(size__icontains=query)
            )

        # Apply price range filters
        if price_min and price_max:
            Posts_Sell_queryset = Posts_Sell_queryset.filter(price__range=(price_min, price_max))
        else:
            if price_min:
                Posts_Sell_queryset = Posts_Sell_queryset.filter(price__gte=price_min)
            if price_max:
                Posts_Sell_queryset = Posts_Sell_queryset.filter(price__lte=price_max)

        # Exclude deleted posts if user is authenticated
        if request.user.is_authenticated:
            deleted_posts = PostSellDeletes.objects.filter(user=request.user).values_list('post', flat=True)
            Posts_Sell_queryset = Posts_Sell_queryset.exclude(id__in=deleted_posts)

        if Posts_Sell_queryset:
            # Serialize and return the post sells
            Posts_Sell_obj_serializer = PostSerializerForGetForMap(Posts_Sell_queryset, many=True, context={'request': request})
            return Response(Posts_Sell_obj_serializer.data, status=200)
        else:
            return Response("No posts found", status=200)


# API view to retrieve all post sells of a user
class AllPostOfOneUser(APIView):
    """
    API view to retrieve all post sells of a user.
    """

    def get(self, request, format=None):
        """
        Retrieve all post sells of a user.
        """
        profile_id = request.GET.get('id')
        profile = get_object_or_404(Profile, id=profile_id)
        posts = PostSell.objects.filter(poster=profile).order_by('-time')

        if posts:
            # Serialize and return the posts
            postsSerilizer = PostSerializerForEachUser(posts, many=True, context={'request': request})
            return Response(postsSerilizer.data, status=200)
        else:
            return Response("No posts found", status=200)


# API view to retrieve detailed information about a specific post sell
class PostsSellDetailedView(APIView):
    """
    API view to retrieve detailed information about a specific post sell.
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, format=None):
        """
        Retrieve detailed information about a specific post sell.
        """
        post_obj = PostSell.objects.filter(id=request.data['id']).first()

        if post_obj:
            # Serialize and return the post sell
            Posts_Sell_obj_serializer = PostSerializerForGet(post_obj, context={'request': request})
            return Response(Posts_Sell_obj_serializer.data, status=200)

        return Response("No post to show", status=403)


# API view to retrieve pictures of a post sell for viewing
class PostPicturesSerilizerforViewingView(APIView):
    """
    API view to retrieve pictures of a post sell for viewing.
    """

    def get(self, request, format=None):
        """
        Retrieve pictures of a post sell.
        """
        post_id = request.query_params.get('post_id')
        post_pictures = PostSellPictures.objects.filter(post_id=post_id)

        # Serialize and return the post pictures
        post_pictures_serializer = PostPicturesSerilizerforViewing(post_pictures, many=True, context={'request': request})
        return Response(post_pictures_serializer.data, status=200)


# API view to create post sell pictures
class PostPicturesSerilizerforCreatingView(generics.CreateAPIView):
    """
    API view to create post sell pictures.
    """

    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)
    model = PostSellPictures
    serializer_class = PostPicturesSerilizerforViewing


# API view to create a post sell
class PostSellForPostingView(generics.CreateAPIView):
    """
    API view to create a post sell.
    """

    queryset = PostSell.objects.all()
    serializer_class = PostSerializerForPosting
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """
        Perform creation of a post sell.
        """
        poster = Profile.objects.filter(user=self.request.data['poster']).first()
        post = serializer.save(poster=poster)
        picture_data = self.request.data.get('pictures', [])

        # Create post sell pictures
        for picture in picture_data:
            PostSellPictures.objects.create(post=post, **picture)


# API view to get liked posts per user per post
class GetLikedPostsPerUserPerPostView(APIView):
    """
    API view to get liked posts per user per post.
    """

    def get(self, request):
        """
        Get liked posts per user per post.
        """
        user_id = request.query_params.get('userId')
        post_id = request.query_params.get('postId')

        likes = PostSellLikes.objects.filter(user=user_id, post=post_id)
        liked_posts = [like for like in likes]
        serializer = PostLikesSerializer(liked_posts, many=True, context={'request': request})
        return Response(serializer.data)


# API view to get liked posts per user
class GetLikedPostsPerUserView(APIView):
    """
    API view to get liked posts per user.
    """

    def get(self, request):
        """
        Get liked posts per user.
        """
        user_id = request.query_params.get('userId')

        likes = PostSellLikes.objects.filter(user=user_id)
        liked_posts = [like for like in likes]
        serializer = PostLikesSerializer(liked_posts, many=True, context={'request': request})
        return Response(serializer.data)


# API view to like a post
class LikePostView(generics.CreateAPIView):
    """
    API view to like a post.
    """

    serializer_class = PostLikesSerializerForCreate
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)


# API view to unlike a post
class LikePostDeleteView(generics.DestroyAPIView):
    """
    API view to unlike a post.
    """

    queryset = PostSellLikes.objects.all()
    serializer_class = PostLikesSerializerForCreate
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def destroy(self, request, *args, **kwargs):
        """
        Delete the like on a post.
        """
        post_id = self.kwargs['post_id']
        user_id = self.kwargs['user_id']
        like = PostSellLikes.objects.filter(post_id=post_id, user_id=user_id).first()
        if like:
            like.delete()
            return Response('success')
        else:
            return Response('This post was not liked')


# API view to get deleted posts per user per post
class GetDeletedPostsPerUserPerPostView(APIView):
    """
    API view to get deleted posts per user per post.
    """

    def get(self, request):
        """
        Get deleted posts per user per post.
        """
        user_id = request.query_params.get('userId')
        post_id = request.query_params.get('postId')

        deletes = PostSellDeletes.objects.filter(user=user_id, post=post_id)
        deleted_posts = [deleteitem for deleteitem in deletes]
        serializer = PostDeletesSerializer(deleted_posts, many=True, context={'request': request})
        return Response(serializer.data)


# API view to get deleted posts per user
class GetDeletedPostsPerUserView(APIView):
    """
    API view to get deleted posts per user.
    """

    def get(self, request):
        """
        Get deleted posts per user.
        """
        user_id = request.query_params.get('userId')

        deletes = PostSellDeletes.objects.filter(user=user_id)
        deleted_posts = [deleteitem for deleteitem in deletes]
        serializer = PostDeletesSerializer(deleted_posts, many=True, context={'request': request})
        return Response(serializer.data)


# API view to delete a post
class DeletePostView(generics.CreateAPIView):
    """
    API view to delete a post.
    """

    serializer_class = PostDeletesSerializerForCreate
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)


# API view to get received interest per user per post
class GetReceivedInterestPerUserPerPostView(APIView):
    """
    API view to get received interest per user per post.
    """

    def get(self, request):
        """
        Get received interest per user per post.
        """
        user_id = request.query_params.get('userId')
        post_id = request.query_params.get('postId')

        interest = PostSellReceivedInterest.objects.filter(user=user_id, post=post_id)
        received_interest = [interest_item for interest_item in interest]
        serializer = RecievedInterestSerializer(received_interest, many=True, context={'request': request})
        return Response(serializer.data)


# API view to get received interest per user
class GetReceivedInterestPerUserView(APIView):
    """
    API view to get received interest per user.
    """

    def get(self, request):
        """
        Get received interest per user.
        """
        user_id = request.query_params.get('userId')

        interest = PostSellReceivedInterest.objects.filter(user=user_id)
        received_interest = [interest_item for interest_item in interest]
        serializer = RecievedInterestSerializer(received_interest, many=True, context={'request': request})
        return Response(serializer.data)


# API view to create received interest
class ReceivedInterestCreateView(generics.CreateAPIView):
    """
    API view to create received interest.
    """

    serializer_class = RecievedInterestSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)


# API view to delete received interest
class ReceivedInterestDeleteView(generics.DestroyAPIView):
    """
    API view to delete received interest.
    """

    queryset = PostSellReceivedInterest.objects.all()
    serializer_class = RecievedInterestSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def destroy(self, request, *args, **kwargs):
        """
        Delete the received interest.
        """
        post_id = self.kwargs['post_id']
        user_id = self.kwargs['user_id']
        interest = PostSellReceivedInterest.objects.filter(post_id=post_id, user_id=user_id).first()
        if interest:
            interest.delete()
            return Response('success')
        else:
            return Response('This interest was not received')


