from django.shortcuts import render, redirect, get_object_or_404
from masterData.forms import CountryForm
from users.models import Country
from django.contrib import messages

def countries_list(request):
    countries = Country.objects.all().order_by('created_at')
    form = CountryForm()
    return render(request, 'masterData/countries_list.html', {'countries': countries, 'form': form})

def create_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Das Land wurde erfolgreich erstellt!")
            return redirect('countries_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('countries_list')


def update_country(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('countries_list')

def delete_country(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('countries_list')