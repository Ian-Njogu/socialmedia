from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Follow, Post, Comment, Like
from users.models import User
from users.serializers import UserSerializer  

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
        
    def get_likes_count(self, obj):
        return obj.like_set.count()  # Changed from 'likes' to 'like_set' (default related_name)
    
    def get_comments_count(self, obj):
        return obj.comments.count()  # Assuming you have related_name='comments' in your Comment model
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_set.filter(user=request.user).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'post', 'created_at')

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_set.filter(user=request.user).exists()
        return False

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('follower', 'created_at')

class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        
        if request.user.id == user_to_follow.id:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.method == 'POST':
            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                followed=user_to_follow
            )
            if created:
                return Response(
                    {'status': 'following'}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'status': 'already following'}, 
                status=status.HTTP_200_OK
            )
        
        elif request.method == 'DELETE':
            deleted, _ = Follow.objects.filter(
                follower=request.user,
                followed=user_to_follow
            ).delete()
            
            if deleted:
                return Response(
                    {'status': 'unfollowed'}, 
                    status=status.HTTP_200_OK
                )
            return Response(
                {'status': 'not following'}, 
                status=status.HTTP_404_NOT_FOUND
            )