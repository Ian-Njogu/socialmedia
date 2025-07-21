"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet, CommentViewSet, FollowViewSet, SearchViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'search/users', SearchViewSet, basename='search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    
    # Manual routes for nested endpoints without regex
     path('posts/<int:post_id>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('users/<int:pk>/follow/', FollowViewSet.as_view({
        'post': 'follow',
        'delete': 'unfollow'
    })),
]