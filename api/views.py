from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment, Like, Follow
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, UserSerializer
from users.models import User

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(post=post, user=request.user)
            if created:
                return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'already liked'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            Like.objects.filter(post=post, user=request.user).delete()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post__id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user, post=post)
        
    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, post_id=None, pk=None):
        comment = self.get_object()
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(comment=comment, user=request.user)
            if created:
                return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'already liked'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            Like.objects.filter(comment=comment, user=request.user).delete()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)

class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post', 'delete'])
    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
            if created:
                return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'already following'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            Follow.objects.filter(follower=request.user, followed=user_to_follow).delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        
class SearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = request.query_params.get('query', '')
        users = User.objects.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
