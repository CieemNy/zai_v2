from django.db import models


class Film(models.Model):
    tytul = models.CharField(max_length=64, blank=False, unique=True)
    rok = models.PositiveSmallIntegerField(blank=False)
    opis = models.TextField(default="")
    premiera = models.DateField(null=True, blank=True)
    imdb_pkts = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.tytul, str(self.rok))


class ExtraInfo(models.Model):
    GATUNEK = {
        (0, 'Inne'),
        (1, 'Horror'),
        (2, 'Komedia'),
        (3, 'Sci-fi'),
        (4, 'Dramat')
    }
    czas_trwania = models.PositiveSmallIntegerField(null=True, blank=True)
    gatunek = models.PositiveSmallIntegerField(choices=GATUNEK, null=True, blank=True)
    rezyser = models.CharField(max_length=50, blank=True, null=True)


class Ocena(models.Model):
    recenzja = models.TextField(default="", blank=True)
    gwiazdki = models.PositiveSmallIntegerField(default=5)


class Aktor(models.Model):
    imie = models.CharField(max_length=32)
    nazwisko = models.CharField(max_length=32)