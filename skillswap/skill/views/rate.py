from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.models import Rating, Comment

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_ratings(request):
    ratings = Rating.objects.all().order_by('-created_at')
    status_choices = Rating.Status.choices
    return render(request, 'skill/rate/index.html', {
        'ratings': ratings,
        'status_choices': status_choices
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_rating(request, pk):
    if request.method == 'POST':
        rating = get_object_or_404(Rating, pk=pk)
        rating.score = request.POST.get('score')
        rating.comment = request.POST.get('comment')
        rating.status = request.POST.get('status')
        rating.save()
        messages.success(request, "Bewertung erfolgreich aktualisiert.")
    return redirect('manage_ratings')

@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_rating_hide(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if rating.status == Rating.Status.HIDDEN:
        rating.status = Rating.Status.PUBLISHED
    else:
        rating.status = Rating.Status.HIDDEN
    rating.save()
    messages.success(request, f"Status für Bewertung von {rating.author} geändert.")
    return redirect('manage_ratings')

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_rating(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    rating.delete()
    messages.success(request, "Bewertung wurde dauerhaft gelöscht.")
    return redirect('manage_ratings')



# comment
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_admin_reply(request, rating_id):
    if request.method == 'POST':
        rating = get_object_or_404(Rating, id=rating_id)
        content = request.POST.get('reply_content')
        if content:
            Comment.objects.create(
                rating=rating,
                author=request.user,
                content=content,
                is_admin_reply=True
            )
            messages.success(request, "Antwort wurde erfolgreich hinzugefügt.")
    return redirect('manage_ratings')


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Kommentar wurde gelöscht.")
    return redirect('manage_ratings')