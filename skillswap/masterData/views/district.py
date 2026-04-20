from django.shortcuts import render, redirect, get_object_or_404
from masterData.forms import DistrictForm
from users.models import City,District
from django.contrib import messages


def districts_list(request):
    districts = District.objects.all().order_by('created_at')
    cities = City.objects.all()
    form = DistrictForm()
    return render(request, 'masterData/districts_list.html', {
        'districts': districts,
        'cities': cities,
        'form': form
    })


def create_district(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "wurde erfolgreich erstellt!")
            return redirect('districts_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('districts_list')


def update_district(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == 'POST':
        form = DistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('districts_list')


def delete_district(request, pk):
    district = get_object_or_404(District, pk=pk)
    district.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('districts_list')
