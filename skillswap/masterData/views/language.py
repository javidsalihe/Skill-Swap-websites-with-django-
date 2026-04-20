from django.shortcuts import render, redirect, get_object_or_404
from masterData.forms import LanguageForm
from users.models import Language
from django.contrib import messages

def languages_list(request):
    languages = Language.objects.all().order_by('created_at')
    form = LanguageForm()
    return render(request, 'masterData/langauges_list.html', {'languages': languages, 'form': form})

def create_language(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Die Sprache wurde erfolgreich erstellt!")
            return redirect('languages_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('languages_list')


def update_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('languages_list')

def delete_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    language.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('languages_list')