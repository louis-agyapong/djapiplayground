from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data["password"]

        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(password)
        user.save()
        return user
