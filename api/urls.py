from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path('artists/', views.NewReleasesView.as_view(), name='new_releases')
]
