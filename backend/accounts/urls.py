from django.contrib.auth import views as auth_views
from django.urls import path, register_converter

from .converters import SignedIntConverter
from .views import (
    HomePage,
    ProfileDetailView,
    ProfileUpdateSuccessView,
    ProfileUpdateView,
    RegistrationSuccessView,
    UserRegistrationView,
    VerifyUser,
    profile_redirect,
)

register_converter(SignedIntConverter, 'signed_pk')

urlpatterns = [

    path('', HomePage.as_view(), name='homepage'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('profile-redirect/', profile_redirect, name='profile_redirect'),         
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
        
    path('profile/<signed_pk:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('success/', RegistrationSuccessView.as_view(), name='register_success'),

    path('activate/<signed_pk:user_id>/<token>', VerifyUser.as_view(), name='activate_user'),

    
    path('profile/edit/success/', ProfileUpdateSuccessView.as_view(), name='profile_edit_success'),
           
]




