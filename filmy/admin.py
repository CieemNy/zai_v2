from django.contrib import admin
from .models import Film


class FilmAdmin(admin.ModelAdmin):
    list_display = ['id', 'tytul', 'rok', 'opis', 'premiera', 'imdb_pkts']


admin.site.register(Film, FilmAdmin)
