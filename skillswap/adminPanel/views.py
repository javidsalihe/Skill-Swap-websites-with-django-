from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Avg
from users.models import User, Skill, Exchange, ExchangeRequest, Rating
import json


def index(request):
    return render(request,'adminPanel/layouts/base.html')


@staff_member_required(login_url='/login/')
def dashboard(request):

    gender_stats = list(User.objects.values('gender').annotate(count=Count('id')))
    district_stats = list(User.objects.values('address_id__district__district_name').annotate(count=Count('id')))
    language_stats = list(User.objects.values('preferred_language__language_name').annotate(count=Count('id')))

    offered_skills = list(
        ExchangeRequest.objects.values('offered_skill__skill_id__name').annotate(count=Count('id'))[:10])

    requested_skills = list(ExchangeRequest.objects.values('requested_skill__name').annotate(count=Count('id'))[:10])

    exchange_status = list(Exchange.objects.values('status').annotate(count=Count('id')))
    urgency_stats = list(ExchangeRequest.objects.values('urgency_level').annotate(count=Count('id')))
    time_range_stats = list(ExchangeRequest.objects.values('preferred_time_range').annotate(count=Count('id')))


    days_map = {}
    all_days = ExchangeRequest.objects.exclude(preferred_days__isnull=True).values_list('preferred_days', flat=True)
    for days_list in all_days:
        if isinstance(days_list, list):
            for day in days_list:
                days_map[day] = days_map.get(day, 0) + 1
    formatted_days = [{'day': k, 'count': v} for k, v in days_map.items()]

    rating_stats = list(Rating.objects.values('score').annotate(count=Count('id')).order_by('score'))

    context = {
        'gender_data': json.dumps(gender_stats),
        'district_data': json.dumps(district_stats),
        'language_data': json.dumps(language_stats),
        'offered_skills_data': json.dumps(offered_skills),
        'requested_skills_data': json.dumps(requested_skills),
        'exchange_status_data': json.dumps(exchange_status),
        'urgency_data': json.dumps(urgency_stats),
        'time_data': json.dumps(time_range_stats),
        'days_data': json.dumps(formatted_days),
        'rating_data': json.dumps(rating_stats),
    }
    return render(request, 'adminPanel/layouts/dashboard.html', context)