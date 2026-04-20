from skill.forms import SkillCategoryForm, SkillForm
from users.models import User, SkillCategory, Skill
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def skill_list(request):
    skills = Skill.objects.select_related('skill_category_id').all().order_by('created_at')
    skill_categories = SkillCategory.objects.all().order_by('created_at')
    form = SkillForm()
    return render(request, 'skill/skill/index.html', {'skills': skills, 'form': form, 'skill_categories': skill_categories})


def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill wurde erfolgreich erstellt!")
            return redirect('skill_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('skill_list')
def update_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('skill_list')
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    messages.warning(request, "wurde gelöscht")
    return redirect('skill_list')
