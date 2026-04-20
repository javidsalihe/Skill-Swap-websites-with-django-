from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from skill.forms import ExchangeRequestForm
from users.models import Exchange, ExchangeRequest, Skill, UserSkill
from django.contrib.auth.decorators import login_required


@login_required
def exchanges(request):
    exchanges = (
        ExchangeRequest.objects
        .select_related('requested_skill', 'offered_skill')
        .filter(requester=request.user)
    )
    skills = Skill.objects.all()
    user_skills = UserSkill.objects.all()
    form = ExchangeRequestForm(user=request.user)

    context = {
        'exchanges': exchanges,
        'user_skills': user_skills,
        'skills': skills,
        'form': form,
    }
    return render(request, 'skill/exchange/index.html', context)




@login_required
def create_exchange_request(request):
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, user=request.user)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.requester = request.user
            exchange.save()
            messages.success(request, "Wurde erfolgreich erstellt!")
            return redirect('exchanges')
        else:
            print("FORM ERRORS:", form.errors)  # 👈 مهم
            messages.error(request, form.errors)
            # messages.error(request, "Fehler: Bitte korrigieren Sie die markierten Felder.")
    return redirect('exchanges')
@login_required
def delete_exchange_request(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk)
    exchange.delete()
    messages.warning(request, "wurde erfolgreich entfernt.")
    return redirect('exchanges')
@login_required
def update_exchange_request(request, pk):
    exchange_instance = get_object_or_404(ExchangeRequest, pk=pk)
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, instance=exchange_instance)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.requester = request.user
            exchange.save()
            messages.success(request, "Ihre Änderungen wurden erfolgreich gespeichert.")
        else:
            error_msg = "Fehler beim Speichern: " + str(form.errors)
            messages.error(request, error_msg)
    return redirect('exchanges')

