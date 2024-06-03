from django.urls import path

from .views import Univers

urlpatterns = [
    path('', Univers.as_view()),
]
