from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (DeleteView, DetailView, FormView, ListView,
                                  TemplateView)

from .forms import CardGenerationForm, CardSearchForm, CardSeriesCreationForm
from .models import Card, CardSeries
from .utils import generate_cards


class IndexView(TemplateView):
    template_name = "index.html"


class CardSeriesListView(ListView):
    model = CardSeries
    template_name = "card_series_list.html"


class CardListView(ListView):
    model = Card
    template_name = "card_list.html"
    paginate_by = settings.CARDS_PER_PAGE_NUMBER

    def get_queryset(self):
        return Card.objects.select_related("series").order_by("id").all()


class CardDetailView(DetailView):
    template_name = "card_detail.html"

    def get_queryset(self):
        return Card.objects.select_related("series").all()


class CardDeleteView(DeleteView):
    model = Card
    template_name = "card_confirm_delete.html"
    success_url = reverse_lazy("cards:index")


class CardTransactionListView(ListView):
    template_name = "card_transactions.html"
    context_object_name = "transaction_list"

    def get_queryset(self):
        card = get_object_or_404(Card, pk=self.kwargs.get("pk"))
        return card.transactions.all()


class GenerateCardsFormView(FormView):
    form_class = CardGenerationForm
    template_name = "generate_cards.html"
    success_url = reverse_lazy("cards:card_list")

    def form_valid(self, form):
        series = form.cleaned_data.get("series")
        cards_count = form.cleaned_data.get("count")
        generate_cards(card_series=series, cards_count=cards_count)
        return super().form_valid(form)


class CardSeriesCreationFormView(FormView):
    form_class = CardSeriesCreationForm
    template_name = "create_card_series.html"
    success_url = reverse_lazy("cards:card_series_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def card_search_view(request):
    form = CardSearchForm(request.POST or None)
    if form.is_valid():
        search_query_params = {
            key: value for key, value in form.cleaned_data.items() if value is not None
        }
        object_list = (Card.objects
                           .filter(**search_query_params)
                           .select_related("series"))
        return render(
            request, "card_search_result_list.html", {
                "object_list": object_list
            }
        )
    return render(request, "card_search.html", {"form": form})


def activate_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    card.is_active = True
    card.save()
    return redirect(reverse("cards:card_detail", args=(pk,)))


def deactivate_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    card.is_active = False
    card.save()
    return redirect(reverse("cards:card_detail", args=(pk,)))
