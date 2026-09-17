from django.urls import path
from interface.home.view.home_view import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
