from django.contrib import admin
from .models import Film, ExtraInfo, Ocena, Aktor

admin.site.register(Aktor)


class ExtraInfoInline(admin.TabularInline):
    model = ExtraInfo


class OcenaInline(admin.TabularInline):
    model = Ocena
    extra = 0


class AktorInline(admin.TabularInline):
    model = Aktor.filmy.through
    extra = 0


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [ExtraInfoInline, OcenaInline, AktorInline]
