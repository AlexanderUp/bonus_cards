from django.db.models import Max

from .models import Card


def get_next_card_number_in_series(card_series):
    next_card_number = 1
    if card_series.cards.count():
        max_number_dict = card_series.cards.aggregate(max_number=Max("number"))
        next_card_number = max_number_dict["max_number"] + 1
    return next_card_number  # noqa


def generate_cards(card_series, cards_count):
    next_number = get_next_card_number_in_series(card_series)
    cards = [
        Card(
            series=card_series,
            number=(next_number + i),
        ) for i in range(cards_count)
    ]
    Card.objects.bulk_create(cards)
