from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.otp_verification_view, name='otp_verification'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Success pages
    path('register-success/', views.register_success, name='register_success'),
    path('otp-success/', views.otp_success, name='otp_success'),
    path('login-success/', views.login_success, name='login_success'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_otp_view, name='reset_password'),  # ✅ Use this
    
    path('reset-password-done/', views.reset_done, name='reset_done'),
    path('logout-success/', views.logout_success, name='logout_success'),




]
