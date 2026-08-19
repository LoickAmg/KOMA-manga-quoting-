from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.home, name="home"),
    path("parcourir/", views.browse, name="browse"),
    path("citation/<int:pk>/", views.quote_detail, name="detail"),
]

api_urlpatterns = [
    path("quotes/", views.QuoteListAPIView.as_view(), name="api-list"),
    path("quotes/random/", views.RandomQuoteAPIView.as_view(), name="api-random"),
    path("quotes/<int:pk>/", views.QuoteDetailAPIView.as_view(), name="api-detail"),
]
