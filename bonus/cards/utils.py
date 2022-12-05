from django.db.models import Max

from .models import Card


def get_next_card_number_in_series(card_series):
    next_card_number = 1
    if card_series.cards:
        max_number_dict = card_series.cards.aggregate(max_number=Max("number"))
        next_card_number = max_number_dict["max_number"] + 1
    return next_card_number  # noqa


def generate_cards(card_series, duration_type, card_count):
    next_number = get_next_card_number_in_series(card_series)
    import sys
    print("generate_cards called", file=sys.stderr)
    cards = [
        Card(
            series=card_series,
            number=(next_number + i),
            duration_type=duration_type
        ) for i in range(card_count)
    ]
    Card.objects.bulk_create(cards)
