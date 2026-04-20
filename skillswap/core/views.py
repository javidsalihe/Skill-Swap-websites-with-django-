from django.shortcuts import render
from users.models import Rating

def index(request):
    latest_ratings = Rating.objects.filter(
        status=Rating.Status.PUBLISHED
    ).select_related('author').order_by('-created_at')[:30]

    context = {
        'latest_ratings': latest_ratings,
    }
    return render(request, 'core/index.html', context)

def dashboard(request):
    return render(request, 'adminPanel/layouts/base.html')


def search_results_view(request):

    skill = request.GET.get('skill', '')
    postal_code = request.GET.get('postalcode', '')
    context = {'skill': skill, 'postal_code': postal_code}
    return render(request, 'skill/exchange/skill_search.html',context )