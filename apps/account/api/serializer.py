from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"error": "Password1 and Password2 should be the same"}
            )

        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(password)
        user.save()
        return user
