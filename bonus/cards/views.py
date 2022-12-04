from django.conf import settings
from django.views.generic import ListView, TemplateView

from .models import Card


class IndexView(TemplateView):
    template_name = "index.html"


class CardListView(ListView):
    model = Card
    template_name = "card_list.html"
    paginate_by = settings.CARDS_PER_PAGE_NUMBER

    def get_queryset(self):
        return Card.objects.select_related("series").all()
