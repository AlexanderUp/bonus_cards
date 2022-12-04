from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path("card_list/", views.CardListView.as_view(), name="card_list"),
    path("", views.IndexView.as_view(), name="index"),
]
