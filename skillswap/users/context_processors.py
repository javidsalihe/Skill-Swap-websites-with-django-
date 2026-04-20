from django.db.models import Q
from users.models import Exchange

def notifications(request):
    if not request.user.is_authenticated:
        return {}

    unread_count = Exchange.objects.filter(
        (Q(user_x=request.user) | Q(user_y=request.user)),
        is_seen_by_receiver=False
    ).exclude(initiated_by=request.user).count()

    return {
        'unread_requests_count': unread_count
    }