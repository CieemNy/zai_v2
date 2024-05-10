from django.forms import ModelForm
from filmy.models import Film


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ['tytul', 'rok', 'opis', 'premiera', 'imdb_pkts']