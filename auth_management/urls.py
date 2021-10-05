from django.urls import path

from . import views


app_name = 'auth_management'

urlpatterns = [
    path('get-spotify-url/', views.getAuthUrl.as_view())
]
