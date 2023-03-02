from rest_framework import serializers

from apps.watchlist.models import Movie, Review, StreamingPlatform

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    title_length = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_title_length(self, obj):
        return len(obj.title)


class StreamingPlatformSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50, validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         """
#         Create and return a new  `Movie` instance, given the validated data
#         """
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Create and return an existing Movie instance, given the validated data
#         """
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.active = validated_data.get("active", instance.active)
#         instance.save()
#         return instance
