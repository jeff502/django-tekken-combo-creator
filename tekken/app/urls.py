from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("download_combo/", views.download_combo, name="download-combo")
]