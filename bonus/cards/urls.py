from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path("card_list/", views.CardListView.as_view(), name="card_list"),
    path(
        "card_detail/<int:pk>/",
        views.CardDetailView.as_view(),
        name="card_detail"
    ),
    path(
        "card/<int:pk>/activate/", views.activate_card, name="activate_card"
    ),
    path(
        "card/<int:pk>/deactivate/",
        views.deactivate_card,
        name="deactivate_card"
    ),
    path(
        "card/<int:pk>/delete/",
        views.CardDeleteView.as_view(),
        name="delete_card"
    ),
    path(
        "card/<int:pk>/view_transaction",
        views.CardTransactionListView.as_view(),
        name="view_card_transaction"
    ),
    path(
        "generate_cards/",
        views.GenerateCardsFormView.as_view(),
        name="generate_cards"
    ),
    path("", views.IndexView.as_view(), name="index"),
]
