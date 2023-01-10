from django.urls import path

from .views import polls_details, polls_list

app_name = "polls"

urlpatterns = [
    path("polls/", polls_list, name="list"),
    path("polls/<int:pk>/", polls_details, name="detail"),
]
