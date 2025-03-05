from django.urls import path
from .views import RegisterView, LoginView, SearchView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),
]