from rest_framework.views import APIView
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

class UserLogout(APIView):
    """
    User Logout
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        if token:
            token.delete()
            return Response({"detail": "You're logged out."}, status=status.HTTP_200_OK)
        return Response({"detail": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegister(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Override Post Function to respond with user's token
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, token_key = serializer.save()
            return Response({'token': token_key}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(generics.UpdateAPIView):
    """
    Change User Password
    """
    model = User
    serializer_class = ChangePasswordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(request.data['new_password'])
            self.object.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
