from django.urls import re_path
from interface.auth.view.auth_view import (
    RegisterView, LoginView, LogoutView, RefreshView,
    ForgotPasswordView, ResetPasswordView,
    VerifyEmailView, VerifyPhoneView, AuthMeView,
)

urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='auth-register'),
    re_path(r'^login/?$', LoginView.as_view(), name='auth-login'),
    re_path(r'^logout/?$', LogoutView.as_view(), name='auth-logout'),
    re_path(r'^refresh/?$', RefreshView.as_view(), name='auth-refresh'),
    re_path(r'^forgot-password/?$', ForgotPasswordView.as_view(), name='auth-forgot-password'),
    re_path(r'^reset-password/?$', ResetPasswordView.as_view(), name='auth-reset-password'),
    re_path(r'^verify-email/?$', VerifyEmailView.as_view(), name='auth-verify-email'),
    re_path(r'^verify-phone/?$', VerifyPhoneView.as_view(), name='auth-verify-phone'),
    re_path(r'^me/?$', AuthMeView.as_view(), name='auth-me'),
]
