from django.urls import path
from .views import *

urlpatterns = [
    path('wszystkie/', wszystkie),
    path('szczegoly/<int:film_id>/', szczegoly),
    path('nowy/', nowy)
]
