from django.urls import path

from .apiviews import ChoiceList, PollDetail, PollList, CreateVote

app_name = "polls"

urlpatterns = [
    path("polls/", PollList.as_view(), name="list"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="detail"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choices"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
]
