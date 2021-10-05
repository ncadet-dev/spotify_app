from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('artists/', views.NewreleasesArtists.as_view())
]
