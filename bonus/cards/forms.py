from django import forms
from django.core.validators import MinValueValidator

from .models import CardSeries


class CardGenerationForm(forms.Form):
    series = forms.ModelChoiceField(
        queryset=CardSeries.objects.all(),
        label="card_series",
        help_text="Select card series",
    )
    count = forms.IntegerField(
        label="cards_count",
        help_text="Input cards count",
        validators=(
            MinValueValidator(1, "Minimum card count to generate is 1."),
        ),
        initial=10,
    )
