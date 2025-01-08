from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    account_no = serializers.IntegerField(read_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth',
                  'department', 'account_no', 'profile_image']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Inactive until email confirmation
        user.save()

        # Create a default profile
        Profile.objects.create(
            user=user,
            account_no=user.id + 1000
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
