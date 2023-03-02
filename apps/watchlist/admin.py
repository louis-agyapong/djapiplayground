from django.contrib import admin

from .models import Movie, Review, StreamingPlatform

admin.site.register(Movie)
admin.site.register(StreamingPlatform)
admin.site.register(Review)
