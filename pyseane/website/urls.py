from django.urls import path
from .views import register

urlpatterns = [
    path('', register, name='register'),
    # Add more URLs as needed
]

