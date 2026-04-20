from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, OuterRef, Exists
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from skill.services.pdf_generator import generate_exchange_pdf
from users.models import ExchangeRequest, Exchange, User, ExchangeNegotiation, Exchange, Rating, Comment
from django.utils import timezone
from django.db import transaction, IntegrityError
from users.models.ExchangeDocument import ExchangeDocument


def swap_skill(request):
    if not request.user.is_authenticated:
        messages.error(request, "Bitte melden Sie sich an.")
        return redirect('login')

    Exchange.objects.filter(
        (Q(user_x=request.user) | Q(user_y=request.user)),
        is_seen_by_receiver=False
    ).exclude(initiated_by=request.user).update(is_seen_by_receiver=True)


    user_rating_exists = Rating.objects.filter(
        exchange=OuterRef('pk'),
        author=request.user
    )

    exchanges = Exchange.objects.filter(
        Q(user_x=request.user) | Q(user_y=request.user)
    ).annotate(
        has_rated=Exists(user_rating_exists)
    ).filter(
        (
            ~Q(status__in=[Exchange.Status.COMPLETED, Exchange.Status.REJECTED, Exchange.Status.CANCELED])
        ) |
        (
                Q(status=Exchange.Status.COMPLETED) & Q(has_rated=False)
        )
    ).select_related(
        'user_x', 'user_y', 'skill_from_x_to_y', 'skill_from_y_to_x',
        'exchange_request'
    ).order_by('-created_at')

    status_choices = [
        (value, label) for value, label in Exchange.Status.choices
        if value != Exchange.Status.PENDING
    ]

    for ex in exchanges:
        ex.my_rating = Rating.objects.filter(
            exchange=ex,
            author=request.user
        ).first()

        ex.other_rating = Rating.objects.filter(
            exchange=ex
        ).exclude(author=request.user).first()

    context = {
        'locations': Exchange.LocationType.choices,
        'exchanges': exchanges,
        'status_choices': status_choices,

    }
    return render(request, 'skill/swap/index.html', context)


def send_exchange_request(request, request_id):
    if not request.user.is_authenticated:
        messages.error(request, "Bitte melden Sie sich an.")
        return redirect('login')

    exchange_request = get_object_or_404(ExchangeRequest, uuid=request_id)

    if exchange_request.requester == request.user:
        messages.error(request, "Sie können keine Anfrage an sich selbst senden.")
        return redirect('searching_result')
    existing_exchange = Exchange.objects.filter(
        exchange_request=exchange_request,
        initiated_by=request.user
    ).first()

    if existing_exchange:
        messages.info(request, "Sie haben für diese Anzeige bereits eine Anfrage gesendet.")
        return redirect('searching_result')

    exchange = Exchange.objects.create(
        user_x=exchange_request.requester,
        user_y=request.user,
        skill_from_x_to_y=exchange_request.offered_skill.skill_id,
        skill_from_y_to_x=exchange_request.requested_skill,
        exchange_request=exchange_request,
        initiated_by=request.user,
        status=Exchange.Status.PENDING,
        is_seen_by_receiver=False
    )
    messages.success(request, f"Anfrage erfolgreich an {exchange_request.requester.get_full_name()} gesendet!")
    return redirect('searching_result')


def skill_swaping_update(request, exchange_uuid):
    if request.method == "POST":
        exchange = get_object_or_404(Exchange, uuid=exchange_uuid)
        status = request.POST.get('status')

        if not status:
            messages.error(request, "Bitte wählen Sie")
            return redirect('swap_skill')

        #  (Rejected / Canceled)
        if status in [Exchange.Status.REJECTED, Exchange.Status.CANCELED]:
            exchange.status = status
            exchange.save()
            messages.success(request, f"Status auf {exchange.get_status_display()} aktualisiert.")

        # (Accepted)
        elif status == Exchange.Status.ACCEPTED:
            negotiation = ExchangeNegotiation.objects.create(
                exchange=exchange,
                proposer=request.user,
                proposed_scheduled_at=request.POST.get('proposed_scheduled_at'),
                proposed_location_type=request.POST.get('proposed_location_type'),
                proposed_meeting_address=request.POST.get('proposed_meeting_address'),
                status=ExchangeNegotiation.NegotiationStatus.ACCEPTED
            )

            exchange.status = Exchange.Status.ACCEPTED
            exchange.scheduled_at = negotiation.proposed_scheduled_at
            exchange.location_type = negotiation.proposed_location_type
            exchange.meeting_address = negotiation.proposed_meeting_address
            exchange.save()
            messages.success(request, "Tausch akzeptiert")

        #  (Completed)
        elif status == Exchange.Status.COMPLETED:
            exchange.status = Exchange.Status.COMPLETED
            exchange.completed_at = timezone.now()
            exchange.save()
            messages.success(request, "Tausch als abgeschlossen markiert.")

    return redirect('swap_skill')


def manage_negotiation(request, exchange_uuid):
    """ثبت پیشنهاد جدید توسط هر یک از طرفین"""
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)

    if request.method == "POST":
        # ابطال پیشنهادهای قبلی که هنوز منتظر پاسخ بودند
        ExchangeNegotiation.objects.filter(exchange=exchange, status='pending').update(status='superseded')

        ExchangeNegotiation.objects.create(
            exchange=exchange,
            proposer=request.user,
            proposed_scheduled_at=request.POST.get('date'),
            proposed_location_type=request.POST.get('location_type'),
            proposed_meeting_address=request.POST.get('address'),
            message=request.POST.get('message'),
            status=ExchangeNegotiation.NegotiationStatus.PENDING
        )
        messages.success(request, "Vorschlag erfolgreich gesendet.")
    return redirect('swap_skill')


def respond_negotiation(request, neg_id, action):
    neg = get_object_or_404(ExchangeNegotiation, id=neg_id)
    exchange = neg.exchange

    # جلوگیری از پاسخ به پیشنهاد خود
    if neg.proposer == request.user:
        messages.error(request, "Ungültige Aktion.")
        return redirect('swap_skill')

    if action == 'accept':
        # ابطال تمام پیشنهادهای قبلی
        exchange.negotiations.filter(status='pending').update(status='superseded')

        neg.status = ExchangeNegotiation.NegotiationStatus.ACCEPTED
        neg.save()

        exchange.scheduled_at = neg.proposed_scheduled_at
        exchange.location_type = neg.proposed_location_type
        exchange.meeting_address = neg.proposed_meeting_address
        exchange.status = Exchange.Status.ACCEPTED
        exchange.save()
        messages.success(request, "Termin wurde erfolgreich akzeptiert.")

        # ----------  PDF  ----------
        if not ExchangeDocument.objects.filter(exchange=exchange, document_type='agreement').exists():
            file_path = generate_exchange_pdf(
                exchange=exchange,
                negotiations=exchange.negotiations.all(),
                ratings=[],
                doc_type='agreement',
                filename=f"agreement_{exchange.uuid}.pdf"
            )
            ExchangeDocument.objects.create(
                exchange=exchange,
                document_type=ExchangeDocument.DocType.AGREEMENT,
                file=file_path,
                generated_by=request.user
            )

    elif action == 'reject':
        neg.status = ExchangeNegotiation.NegotiationStatus.REJECTED
        neg.save()
        messages.info(request, "Vorschlag wurde abgelehnt.")

    return redirect('swap_skill')


def toggle_complete_status(request, exchange_uuid):
    """تایید اتمام کار توسط هر یک از طرفین به صورت جداگانه"""
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)

    if request.user == exchange.user_x:
        exchange.done_by_x = True
        messages.success(request, "Sie haben Ihren Teil der Arbeit bestätigt.")
    elif request.user == exchange.user_y:
        exchange.done_by_y = True
        messages.success(request, "Sie haben Ihren Teil der Arbeit bestätigt.")

    # چک کردن اینکه آیا هر دو طرف کار را تمام کرده‌اند
    if exchange.done_by_x and exchange.done_by_y:
        exchange.status = Exchange.Status.COMPLETED
        exchange.completed_at = timezone.now()
        messages.success(request, "Der gesamte Tausch wurde erfolgreich abgeschlossen!")

    exchange.save()
    return redirect('swap_skill')


def delete_negotiation(request, neg_id):
    """حذف پیشنهاد فقط در صورتی که هنوز پاسخ داده نشده باشد"""
    neg = get_object_or_404(ExchangeNegotiation, id=neg_id, proposer=request.user, status='pending')
    neg.delete()
    messages.success(request, "Vorschlag gelöscht.")
    return redirect('swap_skill')


def update_negotiation(request, neg_id):
    neg = get_object_or_404(ExchangeNegotiation, id=neg_id, proposer=request.user, status='pending')

    if request.method == "POST":
        neg.proposed_scheduled_at = request.POST.get('date')
        neg.proposed_location_type = request.POST.get('location_type')
        neg.proposed_meeting_address = request.POST.get('address')
        neg.message = request.POST.get('message')
        neg.save()
        messages.success(request, "Vorschlag wurde erfolgreich aktualisiert.")
    else:
        messages.error(request, "Ungültige Anfrage.")

    return redirect('swap_skill')


def complete_exchange(request, exchange_uuid):
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)

    if exchange.status not in [Exchange.Status.ACCEPTED, Exchange.Status.COMPLETED]:
        messages.error(request, "Es ist nicht fertig")
        return redirect('swap_skill')

    is_user_x = request.user == exchange.user_x
    is_user_y = request.user == exchange.user_y

    if not (is_user_x or is_user_y):
        messages.error(request, "not allow")
        return redirect('swap_skill')

    # if Rating.objects.filter(exchange=exchange, author=request.user).exists():
    #     messages.warning(request, "Haben sie schon bewertet")
    #     return redirect('swap_skill')

    # score = int(request.POST.get('score'))
    # comment_text = request.POST.get('comment', '')
    duration = int(request.POST.get('actual_duration_minutes', 0))

    completed_at_raw = request.POST.get('completed_at')
    completed_at = timezone.make_aware(
        timezone.datetime.fromisoformat(completed_at_raw)
    ) if completed_at_raw else timezone.now()

    target_user = exchange.user_y if is_user_x else exchange.user_x

    with transaction.atomic():
        if is_user_x:
            exchange.done_by_x = True
            exchange.completed_at_x = completed_at
            exchange.duration_minutes_x = duration
        else:
            exchange.done_by_y = True
            exchange.completed_at_y = completed_at
            exchange.duration_minutes_y = duration

        if exchange.done_by_x and exchange.done_by_y:
            exchange.status = Exchange.Status.COMPLETED
            if exchange.exchange_request:
                ExchangeRequest.objects.filter(
                    Q(requester=exchange.user_x) | Q(requester=exchange.user_y)
                ).update(status=ExchangeRequest.Status.CLOSED)
                # exchange.exchange_request.status = ExchangeRequest.Status.CLOSED
                # exchange.exchange_request.save()

                # ----------  PDF  ----------
                if not ExchangeDocument.objects.filter(exchange=exchange, document_type='completion').exists():
                    file_path = generate_exchange_pdf(
                        exchange=exchange,
                        negotiations=exchange.negotiations.all(),
                        ratings=exchange.ratings.all(),
                        doc_type='completion',
                        filename=f"completion_{exchange.uuid}.pdf"
                    )
                    ExchangeDocument.objects.create(
                        exchange=exchange,
                        document_type=ExchangeDocument.DocType.COMPLETION,
                        file=file_path,
                        generated_by=request.user
                    )

        exchange.save()

    messages.success(request, "wurde erfolgreich gespeichert.")
    return redirect('swap_skill')


@login_required
def rate_exchange(request, exchange_uuid):
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)

    if not (exchange.done_by_x and exchange.done_by_y):
        messages.error(request, "Bewertung erst nach Abschluss beider Seiten möglich.")
        return redirect('swap_skill')

    try:
        Rating.objects.create(
            exchange=exchange,
            author=request.user,
            target_user=exchange.user_y if request.user == exchange.user_x else exchange.user_x,
            score=request.POST['score'],
            comment=request.POST['comment']
        )
        messages.success(request, "Vielen Dank für Ihre Bewertung!")

    except IntegrityError:
        messages.warning(request, "Sie haben bereits bewertet.")

    return redirect('swap_skill')


@login_required
def skill_swap_details(request):
    user = request.user
    exchange_id = request.GET.get('id')

    if exchange_id:
        exchange = get_object_or_404(Exchange,
                                     Q(user_x=user) | Q(user_y=user),
                                     uuid=exchange_id
                                     )
        return render(request, 'skill/swap/skill_swap_details.html', {'exchange': exchange})

    exchanges = Exchange.objects.filter(Q(user_x=user) | Q(user_y=user)).order_by('-created_at')
    return render(request, 'skill/swap/exchange_list.html', {'exchanges': exchanges})

@login_required
def add_exchange_comment(request, rating_id):
    if request.method == 'POST':
        rating = get_object_or_404(Rating, id=rating_id, status='published')
        if rating.author == request.user:
            messages.error(request, "Sie können Ihre eigene Bewertung nicht kommentieren.")
            return redirect(f"/skill/skill_swap_details/?id={rating.exchange.uuid}")

        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                rating=rating,
                author=request.user,
                content=content,
                is_admin_reply=False
            )
            messages.success(request, "Ihr Kommentar wurde erfolgreich hinzugefügt.")
        return redirect(f"/skill/skill_swap_details/?id={rating.exchange.uuid}")

    return redirect('skill_swap_details')


@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_all_exchanges(request):
    exchanges = Exchange.objects.all().select_related(
        'user_x', 'user_y', 'skill_from_x_to_y', 'skill_from_y_to_x'
    ).order_by('-created_at')
    return render(request, 'skill/swap/all_exchange_list.html', {'exchanges': exchanges})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_exchange_admin(request, exchange_uuid):
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)

    if request.method == 'POST':
        exchange.status = request.POST.get('status')
        exchange.location_type = request.POST.get('location_type')
        exchange.meeting_address = request.POST.get('meeting_address')
        exchange.scheduled_at = request.POST.get('scheduled_at') or None
        exchange.actual_duration_minutes = request.POST.get('actual_duration_minutes') or None
        exchange.description = request.POST.get('description')
        exchange.cancellation_reason = request.POST.get('cancellation_reason')

        exchange.done_by_x = 'done_by_x' in request.POST
        exchange.done_by_y = 'done_by_y' in request.POST
        exchange.final_agreement_reached = 'final_agreement_reached' in request.POST

        exchange.save()
        messages.success(request, f"Swap {exchange.uuid} wurde erfolgreich aktualisiert.")
        return redirect('manage_all_exchanges')

    context = {
        'exchange': exchange,
        'status_choices': Exchange.Status.choices,
        'location_choices': Exchange.LocationType.choices,
    }
    return render(request, 'skill/swap/show_and_edit_all_exchange.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_exchange_admin(request, exchange_uuid):
    exchange = get_object_or_404(Exchange, uuid=exchange_uuid)
    exchange.delete()
    messages.success(request, "Der Swap wurde permanent gelöscht.")
    return redirect('manage_all_exchanges')