from .models import Film
from .serializers import *
from rest_framework import generics


class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmRetrieve(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class FilmCreateList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort
