from django.http import HttpResponse
from django.template import loader
from filmy.models import Film
from django.shortcuts import render, redirect, get_object_or_404
from filmy.forms import FilmForm


def wszystkie(request):
    template = loader.get_template("filmy/wszystkie.html")
    wszystkie_filmy = Film.objects.all()
    context = {'wszystkie_filmy': wszystkie_filmy, }
    return HttpResponse(template.render(context, request))


def szczegoly(request, film_id):
    template = loader.get_template("filmy/szczegoly.html")
    film = Film.objects.get(id=film_id)
    context = {'film': film}
    return HttpResponse(template.render(context, request))


def nowy(request):
    nowyform = FilmForm(request.POST or None)
    if nowyform.is_valid():
        nowyform.save()
        return redirect(wszystkie)
    return render(request, 'filmy/c.html', {'nowyform': nowyform})


def edycja(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    form = FilmForm(request.POST or None, instance=film)
    if form.is_valid():
        form.save()
        return redirect(wszystkie)
    return render(request, 'filmy/u.html', {'form': form})
