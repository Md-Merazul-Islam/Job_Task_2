from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserLoginView, activate, UserProfileView,successful,unsuccessful,UserLogOutView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
     path('successful-email-verified/', successful, name='activation_success'),
    path('unsuccessful-email-verified/',unsuccessful, name='activation_failed'),
]
