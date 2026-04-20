from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from pprint import pprint
from skill.forms import SkillCategoryForm
from users.models import User,SkillCategory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def skill_category_list(request):
    skill_categories = SkillCategory.objects.all().order_by('created_at')
    form = SkillCategoryForm()
    return render(request, 'skill/skill_category/index.html', {'skill_categories': skill_categories,'form': form})


def create_skill_category(request):
    if request.method == 'POST':
        form = SkillCategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "kategorie wurde erfolgreich erstellt!")
            return redirect('skill_category_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('skill_category_list')

def update_skill_category(request,pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    if request.method == 'POST':
        form = SkillCategoryForm(request.POST,request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('skill_category_list')

def delete_skill_category(request,pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    category.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('skill_category_list')