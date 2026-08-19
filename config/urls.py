from django.contrib import admin
from django.urls import include, path

from quotes.urls import api_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "quotes"), namespace="api")),
    path("", include("quotes.urls")),
]
