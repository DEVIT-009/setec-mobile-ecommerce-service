from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from infrastructure.persistence.models.user_model import User
from .auth_exception import AuthException
from .jwt_util import JwtUtil
from .user_login_request import UserLoginRequest
from .user_register_request import UserRegisterRequest
from .jwt_authentication import JwtAuthentication
from ..responseutils.response_handler import ResponseHandler


class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, *args, **kwargs):

        serializer = UserLoginRequest(data=request.data)
        if not serializer.is_valid():
            return ResponseHandler.bad_request(
                message="Invalid input", data=serializer.errors
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email, deleted_at__isnull=True).first()
        if not user or not user.check_password(password) or not user.is_active:
            raise AuthException.unauthorized()

        token_value = JwtUtil.generate_token(user)

        return ResponseHandler.success(
            message="Login successful",
            data={"access_token": token_value}
        )


# class RegisterView(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         serializer = UserRegisterRequest(data=request.data)
#         if not serializer.is_valid():
#             return ResponseHandler.bad_request(
#                 message="Invalid input", data=serializer.errors
#             )
#
#         data = serializer.validated_data
#         email = data["email"]
#         password = data["password"]
#         first_name = data["first_name"]
#         last_name = data["last_name"]
#
#         if User.objects.filter(email=email).exists():
#             return ResponseHandler.bad_request(
#                 message="Email already exists",
#                 data={"email": ["Email already exists"]},
#             )
#         base_username = f"{first_name}{last_name}".lower()
#         username = base_username
#         counter = 1
#
#         while User.objects.filter(username=username, deleted_at__isnull=True).exists():
#             username = f"{base_username}{counter}"
#             counter += 1
#
#         role = Role.objects.filter(name="user").first()
#         if not role:
#             return ResponseHandler.bad_request(
#                 message="Default role 'user' not found",
#                 data={"role": ["Default role 'user' not found"]},
#             )
#
#         user = User.objects.create_user(
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#             status=True,
#             is_staff=False,
#             is_superuser=False,
#         )
#         user.roles.set([role])
#
#         return ResponseHandler.created(
#             message="Registered successfully",
#             data={
#                 "id": user.id,
#                 "email": user.email,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "username": user.username,
#                 "roles": [role.name],
#             },
#         )
#
#
# class GetProfileView(APIView):
#     authentication_classes = [JwtAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def get(request, *args, **kwargs):
#         user = request.user
#         user_data = UserResponse.detail(user)
#
#         new_token = JwtUtil.generate_token(user)
#
#         return ResponseHandler.success(
#             message="User profile retrieved successfully",
#             data={
#                 "user": user_data,
#                 "access_token": new_token
#             }
#         )
#
#
# class LogoutView(APIView):
#     authentication_classes = [JwtAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         return ResponseHandler.success(
#             message="Logout successful",
#             data={}
#         )
#
#
# class SwitchRoleView(APIView):
#     authentication_classes = [JwtAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         """
#         Switch user's active role.
#         Request body: {"role_name": "instructor"}
#         """
#         user = request.user
#         role_name = request.data.get("role_name")
#
#         if not role_name:
#             return ResponseHandler.bad_request(
#                 message="role_name is required",
#                 data={"role_name": ["This field is required"]}
#             )
#
#         # Check if user has this role
#         user_role = user.roles.filter(name=role_name).first()
#         if not user_role:
#             return ResponseHandler.bad_request(
#                 message=f"User does not have '{role_name}' role",
#                 data={"role_name": [f"User does not have '{role_name}' role"]}
#             )
#
#         # Generate token with new role
#         new_token = JwtUtil.generate_token(user, role_name)
#         user_data = UserResponse.detail(user)
#
#         return ResponseHandler.success(
#             message=f"Switched to {role_name} role successfully",
#             data={
#                 "user": user_data,
#                 "current_role": role_name,
#                 "access_token": new_token
#             }
#         )
#
#
# class GetAvailableRolesView(APIView):
#     authentication_classes = [JwtAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def get(request, *args, **kwargs):
#         """
#         Get all available roles for the logged-in user.
#         """
#         user = request.user
#         roles = user.roles.all().values('id', 'name')
#
#         # Generate a refreshed token
#         new_token = JwtUtil.generate_token(user)
#
#         return ResponseHandler.success(
#             message="Available roles retrieved successfully",
#             data={
#                 "roles": list(roles),
#                 "count": user.roles.count(),
#                 "access_token": new_token
#             }
#         )
