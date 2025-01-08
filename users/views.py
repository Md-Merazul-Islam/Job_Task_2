from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework import status, generics
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    ProfileSerializer
)
from django.contrib.auth import logout
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # Save user as inactive
        self.send_activation_email(user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Registration successful. Please check your email for the activation link."
        }, status=status.HTTP_201_CREATED)

    def send_activation_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        print("uid: ", uid)
        print("Token: ", token)
        activation_link = f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}/"
        subject = "Activate Your Account"
        message = f"Hi {user.username},\n\nPlease activate your account:\n{activation_link}"
        send_mail(subject, message, 'no-reply@yourdomain.com', [user.email])


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('activation_success')
    else:
        return redirect('activation_failed')


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        # Validate the incoming data
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Extract username/email and password from request data
        data = request.data
        username_or_email = data.get('username')
        password = data.get('password')
        print(username_or_email, password)
        # Authenticate the user
        user = self.authenticate_user(username_or_email, password)

        if user:
            if user.is_active:
                # Log in the user and return the tokens
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account not activated. Please check your email.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

    def authenticate_user(self, username_or_email, password):
        """
        Authenticate the user based on either username or email.
        """
        try:
            if "@" in username_or_email:
                # Look up by email
                user_obj = User.objects.get(email=username_or_email)
                return authenticate(username=user_obj.username, password=password)
            else:
                # Look up by username
                return authenticate(username=username_or_email, password=password)
        except User.DoesNotExist:
            return None


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


def successful(request):
    return render(request, 'successful.html')


def unsuccessful(request):
    return render(request, 'unsuccessful.html')


class UserLogOutView(APIView):

    def post(self, request):
        try:
            # Automatically log the user out
            logout(request)  # Clear session data and logout the user

            # Optionally, blacklist the refresh token (if provided)
            refresh_token = request.data.get("refresh", None)
            if refresh_token is None:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Invalidate the refresh token

            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
            return Response({'detail': 'Invalid token provided.'}, status=status.HTTP_400_BAD_REQUEST)


# {
#   "refresh": "<your-refresh-token>"
# }
