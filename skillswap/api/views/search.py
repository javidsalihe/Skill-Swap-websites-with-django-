from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models.exchangeRequest import ExchangeRequest
from api.services.geocoding import postal_to_latlng
from django.db.models import Q
from api.utils.distance import haversine


def skill_search_session_save(request):
    skill = request.GET.get("skill", "").strip()
    postal = request.GET.get("postalcode", "").strip()

    if skill and postal:
        request.session['search_data'] = {
            'skill': skill,
            'postalcode': postal
        }


class SkillSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        skill_q = request.GET.get("skill", "").strip()
        postal_q = request.GET.get("postalcode", "").strip()

        if not skill_q or not postal_q:
            return Response([])

        lat, lng = postal_to_latlng(postal_q)
        if lat is None:
            return Response({"error": "Invalid Postal Code"}, status=400)

        exchanges = ExchangeRequest.objects.select_related(
            "requester__address_id",
            "offered_skill__skill_id",
            "requested_skill"
        ).filter(
            Q(offered_skill__skill_id__name__icontains=skill_q) |
            Q(requested_skill__name__icontains=skill_q) |
            Q(title__icontains=skill_q),
            status="available"
        )

        results = []
        for ex in exchanges:
            addr = ex.requester.address_id
            dist = None

            if addr and addr.latitude and addr.longitude:
                dist = haversine(lat, lng, addr.latitude, addr.longitude)

                profile_img = None
                if hasattr(ex.requester, 'profile_image_url') and ex.requester.profile_image_url:
                    try:
                        profile_img = ex.requester.profile_image_url.url
                    except ValueError:
                        profile_img = None

            results.append({
                "uuid": str(ex.uuid),
                # "user_id": ex.requester.id,
                "user": ex.requester.get_full_name() or ex.requester.username,
                "profile_image": profile_img,
                "title": ex.title,
                "offered": ex.offered_skill.skill_id.name if ex.offered_skill else "N/A",
                "requested": ex.requested_skill.name if ex.requested_skill else "N/A",
                "distance_km": round(dist, 1) if dist is not None else None,
                "city": addr.district.city.city_name if addr and addr.district and addr.district.city else "Unbekannt",
                "postal_code": addr.postal_code if addr else "N/A"
            })


        results.sort(key=lambda x: (x["distance_km"] is None, x["distance_km"]))
        return Response(results[:20])

