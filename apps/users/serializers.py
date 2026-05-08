from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )

    password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password_confirm",
            "role",
            "phone",
        ]

    def validate_username(self, value):
        """Validate username is unique and not empty"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Username cannot be empty")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        """Validate email is unique and properly formatted"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Email cannot be empty")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    def validate(self, data):
        """Validate passwords match"""
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "phone",
            "first_name",
            "last_name",
            "is_email_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "is_email_verified",
            "created_at",
            "updated_at",
        ]

    def validate_phone(self, value):
        """Validate phone number format"""
        if value and not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value