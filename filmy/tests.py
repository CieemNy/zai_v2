from django.urls import path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.contrib.auth.models import User
from .views import *
from .models import Film


class TestyURL(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('filmy/', FilmCreateList.as_view(), name='FilmCreateList'),
        path('filmy/<int:pk>/', FilmRetrieveUpdateDestroy.as_view(), name='FilmRetrieveUpdateDestroy'),
        path('extrainfo/', ExtraInfoCreateList.as_view(), name='ExtraInfoCreateList'),
        path('user/', UserCreateList.as_view(), name='UserCreateList'),
        path('user/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='UserRetrieveUpdateDestroy'),
        path('statRezyserLiczbaFilmow/', statRezyserLiczbaFilmow.as_view(), name='statRezyserLiczbaFilmow'),
    ]

    def setUp(self):
        User.objects.create_superuser(username='admin', password='admin')
        self.test_user = User.objects.create_user(id=1, username='test_user', password='password')

    def test_FilmCreateList(self):
        url = reverse('FilmCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmRetrieveUpdateDestroy(self):
        url = reverse('FilmRetrieveUpdateDestroy', args=[1])
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ExtraInfoCreateList(self):
        self.client.login(username='admin', password='admin')
        url = reverse('ExtraInfoCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ListaUzytkownikow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('UserCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UserRetrieveUpdateDestroy(self):
        self.client.login(username='admin', password='admin')
        url = reverse('UserRetrieveUpdateDestroy', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Testy_Widokow(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='admin')

    def test_FilmCreateList_List(self):
        url = reverse('FilmCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmCreateList_Create(self):
        self.client.login(username='admin', password='admin')
        url = reverse('FilmCreateList')
        film = {'tytul': 'Film testowy', 'rok': 2024, 'opis': 'opis'}
        response = self.client.post(url, film, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().rok, 2024)
        self.assertEqual(Film.objects.get().opis, 'opis')

    def test_FilmRetrieveUpdateDestroy_Retrieve(self):
        film = Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        url = reverse('FilmRetrieveUpdateDestroy', args=[film.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')

    def test_FilmRetrieveUpdateDestroy_Update(self):
        self.client.login(username='admin', password='admin')
        film = Film.objects.create(tytul="Film testowy 2", rok=2024, opis="opis", owner=self.superuser)
        url = reverse('FilmRetrieveUpdateDestroy', args=[film.id])
        film_data = {'tytul': 'Film testowy', 'rok': 2020, 'opis': 'opis opis'}
        response = self.client.put(url, film_data, format='json', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().rok, 2020)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().opis, 'opis opis')

    def test_FilmRetrieveUpdateDestroy_Destroy(self):
        self.client.login(username='admin', password='admin')
        film = Film.objects.create(tytul="Film testowy", rok=2024, opis="opis", owner=self.superuser)
        url = reverse('FilmRetrieveUpdateDestroy', args=[film.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Film.objects.count(), 0)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
