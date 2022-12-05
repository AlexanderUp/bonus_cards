from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import CardSeries


class CardSeriesCreationForm(forms.ModelForm):
    class Meta:
        model = CardSeries
        fields = ("duration_type", "description",)


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


class CardSearchForm(forms.Form):
    series__gte = forms.IntegerField(
        min_value=1,
        label="Card series from",
        help_text="Card series from",
        required=False,
    )
    series__lte = forms.IntegerField(
        min_value=1,
        label="Card series to",
        help_text="Card series to",
        required=False,
    )
    number__gte = forms.IntegerField(
        min_value=1,
        label="Card number from",
        help_text="Card number from",
        required=False,
    )
    number__lte = forms.IntegerField(
        min_value=1,
        label="Card number to",
        help_text="Card number to",
        required=False,
    )
    series__issue_date__gte = forms.DateTimeField(
        label="Issued after",
        help_text="Issued after",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    series__issue_date__lte = forms.DateTimeField(
        label="Issued before",
        help_text="Issued before",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    valid__gte = forms.DateTimeField(
        label="Valid after",
        help_text="Valid after",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    valid__lte = forms.DateTimeField(
        label="Valid before",
        help_text="Valid before",
        required=False,
        widget=forms.SelectDateWidget(),
    )

    def clean(self):
        cleaned_data = super().clean()
        series__gte = cleaned_data.get("series__gte")
        series__lte = cleaned_data.get("series__lte")
        number__gte = cleaned_data.get("number__gte")
        number__lte = cleaned_data.get("number__lte")
        series__issue_date__gte = cleaned_data.get("series__issue_date__gte")
        series__issue_date__lte = cleaned_data.get("series__issue_date__lte")
        valid__gte = cleaned_data.get("valid__gte")
        valid__lte = cleaned_data.get("valid__lte")

        if series__gte and series__lte:
            if series__gte > series__lte:
                raise ValidationError("Incorrect series bound!")

        if number__gte and number__lte:
            if number__gte > number__lte:
                raise ValidationError("Incorrect number bound!")

        if series__issue_date__gte and series__issue_date__lte:
            if series__issue_date__gte > series__issue_date__lte:
                raise ValidationError("Incorrect issue date bound!")

        if valid__gte and valid__lte:
            if valid__gte > valid__lte:
                raise ValidationError("Incorrect valid until bound!")

        conditions = (
            series__gte,
            series__lte,
            number__gte,
            number__lte,
            series__issue_date__gte,
            series__issue_date__lte,
            valid__gte,
            valid__lte,
        )

        if not any(conditions):
            raise ValidationError("No conditions specified!")
