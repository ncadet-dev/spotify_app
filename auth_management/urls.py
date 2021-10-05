from django.urls import path

from . import views


app_name = 'auth_management'

urlpatterns = [
    path('get-spotify-url/', views.getAuthUrl.as_view()),
    path('callback/', views.spotify_callback),
    path('is_authenticated/', views.IsAuthenticated.as_view())
]
