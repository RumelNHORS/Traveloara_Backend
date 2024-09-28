from django.urls import path
from userauths import views as userauth_views


urlpatterns = [
    # User Registration
    path('api/register/', userauth_views.UserRegisterView.as_view(), name='register'),
    # User Loggin
    path('api/login/', userauth_views.UserLoginView.as_view(), name='login'),
    # Show All User/ User List
    path('api/users/', userauth_views.UserListView.as_view(), name='user_list'),
    path('api/users/<int:pk>/', userauth_views.UserUpdateView.as_view(), name='user_update'),
]