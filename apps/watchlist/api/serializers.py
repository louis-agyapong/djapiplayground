from rest_framework import serializers
from apps.watchlist.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new  `Movie` instance, given the validated data
        """
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Create and return an existing Movie instance, given the validated data
        """
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance
        