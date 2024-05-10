from .views import FilmList, FilmRetrieve, FilmCreateList
from django.urls import path

urlpatterns = [
    path('filmlist/', FilmList.as_view(), name='FilmList'),
    path('filmretrieve/<int:pk>/', FilmRetrieve.as_view(), name='FilmRetrieve'),
    path('filmcreatelist/', FilmCreateList.as_view(), name='FilmCreateList')
]