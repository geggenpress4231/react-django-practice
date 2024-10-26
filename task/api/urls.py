from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListCreateView, TaskRetrieveUpdateDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT token refresh
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),          # List and create tasks
    path('tasks/<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='task-detail'),  # Retrieve, update, delete tasks
]





