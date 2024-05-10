from django.urls import path
from .views import *

urlpatterns = [
    path('wszystkie/', wszystkie),
    path('szczegoly/', szczegoly),
]
