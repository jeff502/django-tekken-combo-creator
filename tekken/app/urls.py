from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("download/", views.download_combo, name="download-combo"),
    path("remove", views.remove_character, name="remove-character")
    
]