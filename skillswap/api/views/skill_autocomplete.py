from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

import users
from users.models.exchangeRequest import ExchangeRequest


class SkillAutocompleteAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = request.GET.get('q', '').strip()

        if len(q) < 2:
            return Response([])

        exchanges = (
            ExchangeRequest.objects
            .select_related('requested_skill', 'offered_skill__skill_id')
            .filter(
                Q(requested_skill__name__icontains=q) |
                Q(offered_skill__skill_id__name__icontains=q)
            )
        )

        skill_set = set()
        results = []

        for ex in exchanges:
            # requested skill
            if q.lower() in ex.requested_skill.name.lower():
                skill_set.add(ex.requested_skill.name)

            # offered skill
            offered_name = ex.offered_skill.skill_id.name
            if q.lower() in offered_name.lower():
                skill_set.add(offered_name)

        for skill in list(skill_set)[:10]:
            results.append({
                "label": skill
            })
        return Response(results)
