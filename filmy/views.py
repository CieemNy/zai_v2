from .models import Film
from .serializers import FilmModelSerializer
from rest_framework import generics


class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer

