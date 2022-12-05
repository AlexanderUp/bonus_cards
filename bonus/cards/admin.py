from django.contrib import admin

from .models import Card, CardSeries, Transaction


class CardSeriesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "duration_type",
        "issue_date",
        "description",
        "duration",
        "valid_until",
    )
    list_display_links = (
        "description",
    )
    search_fields = (
        "description",
    )
    empty_value_display = "--empty--"


class CardAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "series",
        "number",
        # "issue_date",
        # "duration_type",
        "last_used_date",
        "balance",
        "is_active",
        "humanreadable_status",
        "valid_until",
    )
    list_select_related = (
        "series",
    )
    search_fields = (
        "series__description",
    )
    list_filter = (
        "series__issue_date",
    )
    empty_value_display = "--empty--"


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "card",
        "amount",
        "description",
    )


admin.site.register(CardSeries, CardSeriesAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Transaction, TransactionAdmin)
