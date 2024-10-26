from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

# View for user registration
class RegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# List and Create Tasks
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return tasks for the logged-in user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user as the task creator
        serializer.save(user=self.request.user)

# Retrieve, Update, and Delete Individual Tasks
class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow the user to retrieve or modify their own tasks
        return Task.objects.filter(user=self.request.user)
