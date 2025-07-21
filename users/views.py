from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer

# create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer  # Using RegisterSerializer from users/serializers.py
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)
        login(self.request, user)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Using LoginSerializer from users/serializers.py
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data  # Using UserSerializer from users/serializers.py
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)