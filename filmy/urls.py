from .views import *
from django.urls import path

urlpatterns = [
    path('', api_root),
    path('filmlist/', FilmList.as_view(), name='FilmList'),
    path('filmretrieve/<int:pk>/', FilmRetrieve.as_view(), name='FilmRetrieve'),
    path('filmcreatelist/', FilmCreateList.as_view(), name='FilmCreateList'),
    path('userlist/', UserList.as_view(), name='UserList'),
    path('usercreatelist/', UserCreateList.as_view(), name='UserCreateList')
]
