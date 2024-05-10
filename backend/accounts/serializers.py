from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    "username": user.username,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("User does not exist.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user
