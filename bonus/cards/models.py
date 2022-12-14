from datetime import timedelta
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class CardValidDateAnnotatedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            valid_until_date=(models.F("issue_date") + models.F("duration"))
        )


class CardSeries(models.Model):
    ONE_MONTH = timedelta(30)
    SIX_MONTH = timedelta(183)
    ONE_YEAR = timedelta(365)

    CARD_DURATION_TYPES = [
        (ONE_MONTH, 'One month'),
        (SIX_MONTH, 'Six month'),
        (ONE_YEAR, 'One year'),
    ]

    duration = models.DurationField(
        verbose_name="card_duration_type",
        help_text="Card duration type",
        choices=CARD_DURATION_TYPES,
        default=ONE_MONTH,
    )
    issue_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="issue_date",
        help_text="Card issue date",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="description",
        help_text="Card series description",
    )
    objects = CardValidDateAnnotatedManager()

    class Meta:
        verbose_name = "card_series"
        verbose_name_plural = "card_serieses"
        ordering = ("-id",)

    def __str__(self):
        return f"CardSeries({self.printable_number})"

    @property
    def series(self):
        return self.pk

    @property
    def printable_number(self):
        return f"{self.series:0>5}"

    @property
    def valid_until(self):
        return (self.issue_date + self.duration)

    @property
    def cards_count(self):
        return self.cards.count()


class Card(models.Model):
    NOT_ACTIVATED = 0
    ACTIVATED = 1
    OUTDATED = 2

    HUMANREADABLE_CARD_STATUSES = {
        NOT_ACTIVATED: "Not activated",
        ACTIVATED: "Active",
        OUTDATED: "Outdated",
    }

    series = models.ForeignKey(
        CardSeries,
        related_name="cards",
        on_delete=models.CASCADE,
        verbose_name="series",
        help_text="ID of card series",
    )
    number = models.PositiveIntegerField(
        verbose_name="number",
        help_text="Card number",
        validators=(MinValueValidator(1, "Card numbers start from 1."),),
    )
    last_used_date = models.DateTimeField(
        verbose_name="last_used_date",
        help_text="Date of last card usage",
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="balance",
        help_text="Card balance",
        validators=[MinValueValidator(0, "Balance can not be negative"),],
        default=Decimal(0.0),
    )
    is_active = models.BooleanField(
        verbose_name="is_active",
        help_text="Is card active?",
        default=False,
    )

    class Meta:
        verbose_name = "card"
        verbose_name_plural = "cards"
        ordering = ("-id",)
        constraints = (
            models.CheckConstraint(
                check=models.Q(balance__gte=Decimal(0.0)),
                name="negative_card_balance_disallowed"
            ),
            models.UniqueConstraint(
                fields=("series", "number"),
                name="series_number_pair_to_be_unique"
            ),
        )

    def __str__(self):
        return f"Card({self.printable_number})"

    @property
    def printable_number(self):
        return f"{self.series.printable_number}-{self.number:0>7}"

    @property
    def valid_until(self):
        return self.series.valid_until

    @property
    def duration(self):
        return self.series.duration

    @property
    def status(self):
        if timezone.now() < self.valid_until:
            if self.is_active:
                return Card.ACTIVATED
            return Card.NOT_ACTIVATED
        return Card.OUTDATED

    @property
    def humanreadable_status(self):
        return Card.HUMANREADABLE_CARD_STATUSES.get(self.status)


class Transaction(models.Model):
    card = models.ForeignKey(
        Card,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="card",
        help_text="card",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="amount",
        help_text="Transaction amount",
        default=Decimal(0.0),
    )
    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="date_time",
        help_text="Transaction date and time",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="description",
        help_text="Transaction description",
    )

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        ordering = ("-id",)
        constraints = (
            models.CheckConstraint(
                check=~models.Q(amount=Decimal(0.0)),
                name="zero_amount_transaction_disallowed"
            ),
        )

    def __str__(self):
        return f"Transaction({self.amount})<Card({self.card})>"
