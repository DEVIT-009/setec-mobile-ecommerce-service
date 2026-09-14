from django.urls import path
from interface.home.view.home_view import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
