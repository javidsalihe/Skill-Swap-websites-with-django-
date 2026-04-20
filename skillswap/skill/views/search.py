from django.db.models import Q
from math import radians, cos, sin, asin, sqrt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from users.models import ExchangeRequest, Exchange, User

def calculate_haversine(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]: return None
    R = 6371
    dLat, dLon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
    return round(R * 2 * asin(sqrt(a)), 1)

def searching_result(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_address = request.user.address_id
    if not user_address or not user_address.latitude or not user_address.longitude:
        messages.error(request, "Bitte ergänzen Sie Ihre Adresse in den Einstellungen.")
        return redirect('profile',userId=request.user.id)

    skill = request.GET.get('skill', '')
    postal_code = request.GET.get('postalcode', '')

    query_set = ExchangeRequest.objects.exclude(requester=request.user)

    if skill:
        query_set = query_set.filter(
            Q(offered_skill__skill_id__name__icontains=skill) |
            Q(requested_skill__name__icontains=skill) |
            Q(title__icontains=skill) |
            Q(status__icontains='pending')
        ).distinct()

    if postal_code:
        query_set = query_set.filter(requester__address_id__postal_code__icontains=postal_code)

    results = []
    for exchange in query_set:
        target_user = exchange.requester
        target_address = target_user.address_id

        distance = calculate_haversine(
            user_address.latitude, user_address.longitude,
            target_address.latitude, target_address.longitude
        ) if target_address and target_address.latitude else None

        city_display = "Unbekannt"
        if target_address and target_address.district and target_address.district.city:
            city_obj = target_address.district.city
            # Wir nutzen str(), da das Modell City wahrscheinlich __str__ definiert hat
            city_display = getattr(city_obj, 'name', getattr(city_obj, 'city_name', str(city_obj)))

        results.append({
            'exchange_id': exchange.id,
            'exchange_request_uuid': exchange.uuid,
            'exchange_uuid': exchange.uuid,
            'user_name': target_user.get_full_name() or target_user.username,
            'offered_skill': exchange.offered_skill.skill_id.name if exchange.offered_skill else "N/A",
            'requested_skill': exchange.requested_skill.name if exchange.requested_skill else "N/A",
            'description':exchange.description,
            'title':exchange.title,
            'estimated_duration_minutes':exchange.estimated_duration_minutes,
            'expires_at':exchange.expires_at,
            'max_distance_km':exchange.max_distance_km,
            'urgency_level':exchange.urgency_level,
            'available_days': ", ".join(exchange.preferred_days) if exchange.preferred_days else "Nach Vereinbarung",
            'available_time': exchange.get_preferred_time_range_display() if exchange.preferred_time_range else "Flexibel",
            'plz': target_address.postal_code if target_address else "N/A",
            'distance_km': distance,
            'city': city_display,
            'profile_image_url':target_user.profile_image_url,
            'preferred_language':target_user.preferred_language,
        })
    results = sorted(results, key=lambda x: (x['distance_km'] is None, x['distance_km']))

    return render(request, 'skill/exchange/skill_search.html', {
        'results': results,
        'skill': skill,
        'postal_code': postal_code
    })
