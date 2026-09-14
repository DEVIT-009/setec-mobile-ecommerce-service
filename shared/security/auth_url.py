from django.urls import path

from shared.security.auth_view import (
    AuthView
# ,
#     RegisterView,
#     GetProfileView,
#     LogoutView,
#     SwitchRoleView,
#     GetAvailableRolesView
)

urlpatterns = [
    path("login", AuthView.as_view(), name="auth-login"),
    # path("register", RegisterView.as_view(), name="auth-register"),
    # path("profile", GetProfileView.as_view(), name="auth-get-profile"),
    # path("logout", LogoutView.as_view(), name="auth-logout"),
    # path("switch-role", SwitchRoleView.as_view(), name="auth-switch-role"),
    # path("available-roles", GetAvailableRolesView.as_view(), name="auth-available-roles"),
]
