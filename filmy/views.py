from .models import Film
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmRetrieve(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmCreateList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort


class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'Użytkownicy': reverse('ListaUzytkownikow', request=request, format=format),
        'Wszystkie filmy': reverse('ListaFilmow', request=request, format=format),
        'Informacje dodatkowe': reverse('InformacjeDodatkowe', request=request, format=format),
        'Wszystkie oceny': reverse('Recenzje', request=request, format=format),
        'Wszyscy aktorzy': reverse('Aktorzy', request=request, format=format),
    })