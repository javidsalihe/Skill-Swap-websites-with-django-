from skill.forms import SkillCategoryForm, SkillForm, UserSkillForm
from users.models import User, Skill,UserSkill
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def user_skill_list(request):
    user_skills = UserSkill.objects.select_related('skill_id','user_id').all()
    users = User.objects.all().values('id', 'username', 'first_name', 'last_name')
    skills = Skill.objects.all()
    form = UserSkillForm()
    return render(request, 'skill/user_skill/index.html', {'skills': skills, 'form': form, 'users': users, 'user_skills': user_skills})

def create_user_skill(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Wurde erfolgreich erstellt!")
            return redirect('user_skill_list')
        else:
            messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('user_skill_list')


def update_user_skill(request, pk):
    user_skill = get_object_or_404(UserSkill, pk=pk)
    if request.method == 'POST':
        form = UserSkillForm(request.POST, instance=user_skill)
        if form.is_valid():
            form.save()
            messages.success(request, "bearbeiten war erstellt!")
    return redirect('user_skill_list')


def delete_user_skill(request, pk):
    user_skill = get_object_or_404(UserSkill, pk=pk)
    user_skill.delete()
    messages.warning(request, "Die Kompetenz wurde erfolgreich aus Ihrem Profil entfernt.")
    return redirect('user_skill_list')
