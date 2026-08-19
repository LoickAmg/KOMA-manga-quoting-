import random

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quote, Theme
from .serializers import QuoteSerializer

PAGE_SIZE = 12


def _apply_filters(queryset, request):
    """Filtres partagés par les vues web et API : recherche libre (texte,
    personnage, série), série exacte, thème exact."""
    search = request.GET.get("q", "").strip()
    if search:
        queryset = queryset.filter(
            Q(text__icontains=search)
            | Q(character__icontains=search)
            | Q(series__icontains=search)
        )

    series = request.GET.get("series", "").strip()
    if series:
        queryset = queryset.filter(series=series)

    theme = request.GET.get("theme", "").strip()
    if theme:
        queryset = queryset.filter(theme=theme)

    return queryset


# --- Vues web (Django templates) -------------------------------------------------


def home(request):
    quote = Quote.objects.order_by("?").first()
    return render(request, "quotes/home.html", {"quote": quote})


def browse(request):
    queryset = _apply_filters(Quote.objects.all(), request)
    paginator = Paginator(queryset, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    all_series = Quote.objects.order_by("series").values_list("series", flat=True).distinct()

    base_params = request.GET.copy()
    base_params.pop("page", None)
    base_query = base_params.urlencode()

    context = {
        "page_obj": page_obj,
        "all_series": all_series,
        "themes": Theme.choices,
        "current_q": request.GET.get("q", ""),
        "current_series": request.GET.get("series", ""),
        "current_theme": request.GET.get("theme", ""),
        "base_query": base_query,
    }
    return render(request, "quotes/browse.html", context)


def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, "quotes/detail.html", {"quote": quote})


# --- API REST (Django REST Framework) ---------------------------------------------


class QuoteListAPIView(generics.ListAPIView):
    """GET /api/quotes/ — liste paginée, filtrable via ?q=&series=&theme=."""

    serializer_class = QuoteSerializer

    def get_queryset(self):
        return _apply_filters(Quote.objects.all(), self.request)


class QuoteDetailAPIView(generics.RetrieveAPIView):
    """GET /api/quotes/<id>/"""

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class RandomQuoteAPIView(APIView):
    """GET /api/quotes/random/ — une citation au hasard, respecte les mêmes
    filtres que la liste (utile pour "citation au hasard dans ce thème")."""

    def get(self, request):
        queryset = _apply_filters(Quote.objects.all(), request)
        count = queryset.count()
        if count == 0:
            return Response({"detail": "Aucune citation ne correspond à ces filtres."}, status=404)
        quote = queryset[random.randrange(count)]
        return Response(QuoteSerializer(quote).data)
