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
    series_from = forms.IntegerField(
        min_value=1,
        label="Card series from",
        help_text="Card series from",
        required=False,
    )
    series_to = forms.IntegerField(
        min_value=1,
        label="Card series to",
        help_text="Card series to",
        required=False,
    )
    number_from = forms.IntegerField(
        min_value=1,
        label="Card number from",
        help_text="Card number from",
        required=False,
    )
    number_to = forms.IntegerField(
        min_value=1,
        label="Card number to",
        help_text="Card number to",
        required=False,
    )
    issue_date_from = forms.DateTimeField(
        label="Issued from",
        help_text="Issued from",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    issue_date_to = forms.DateTimeField(
        label="Issued to",
        help_text="Issued to",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    valid_from = forms.DateTimeField(
        label="Valid to min date",
        help_text="Valid to min date",
        required=False,
        widget=forms.SelectDateWidget(),
    )
    valid_to = forms.DateTimeField(
        label="Valid to max date",
        help_text="Valid to max date",
        required=False,
        widget=forms.SelectDateWidget(),
    )

    def clean(self):
        cleaned_data = super().clean()
        series_from = cleaned_data.get("series_from")
        series_to = cleaned_data.get("series_to")
        number_from = cleaned_data.get("number_from")
        number_to = cleaned_data.get("number_to")
        issue_date_from = cleaned_data.get("issue_date_from")
        issue_date_to = cleaned_data.get("issue_date_to")
        valid_from = cleaned_data.get("valid_from")
        valid_to = cleaned_data.get("valid_to")

        if series_from and series_to:
            if series_from > series_to:
                raise ValidationError("Incorrect series bound!")

        if number_from and number_to:
            if number_from > number_to:
                raise ValidationError("Incorrect number bound!")

        if issue_date_from and issue_date_to:
            if issue_date_from > issue_date_to:
                raise ValidationError("Incorrect issue date bound!")

        if valid_from and valid_to:
            if valid_from > valid_to:
                raise ValidationError("Incorrect valid until bound1")

        conditions = (
            series_from, series_to, number_from, number_to,
            issue_date_from, issue_date_to, valid_from, valid_to,
        )

        if not any(conditions):
            raise ValidationError("No conditions specified!")
