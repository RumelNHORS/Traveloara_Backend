from django.urls import path
from userauths import views as userauth_views


urlpatterns = [
    path('api/register/', userauth_views.UserRegisterView.as_view(), name='register'),
    path('api/login/', userauth_views.UserLoginView.as_view(), name='login'),
]