from django.shortcuts import render, redirect, get_object_or_404
from masterData.forms import CityForm
from users.models import City, Country
from django.contrib import messages


def cities_list(request):
    cities = City.objects.all().order_by('created_at')
    countries = Country.objects.all()
    form = CityForm()
    return render(request, 'masterData/cities_list.html', {
        'cities': cities,
        'countries': countries,
        'form': form
    })


def create_city(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "wurde erfolgreich erstellt!")
            return redirect('cities_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('cities_list')


def update_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('cities_list')


def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('cities_list')
