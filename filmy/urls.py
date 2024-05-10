from .views import FilmList
from django.urls import path

urlpatterns = [
    path('filmlist/', FilmList.as_view(), name='FilmList')
]