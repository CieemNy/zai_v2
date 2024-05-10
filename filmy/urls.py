from django.urls import path
from .views import *

urlpatterns = [
    path('wszystkie/', wszystkie),
    path('szczegoly/<int:film_id>/', szczegoly),
    path('nowy/', nowy),
    path('edycja/<int:film_id>', edycja)
]
