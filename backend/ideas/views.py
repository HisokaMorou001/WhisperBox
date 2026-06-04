from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from .models import Idea


@login_required
def home(request):
    ideas = Idea.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'ideas': ideas})


@login_required
def create(request):
    if request.method == "POST":
        Idea.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description']
        )
        return redirect('home')

    return render(request, 'create.html')


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def set_status(request, idea_id, status):
    idea = get_object_or_404(Idea, id=idea_id)

    if status == "approved":
        if idea.status == "approved":
            idea.status = "pending"
            idea.approved_at = None
        else:
            idea.status = "approved"
            idea.approved_at = timezone.now()
            idea.rejected_at = None

    elif status == "rejected":
        if idea.status == "rejected":
            idea.status = "pending"
            idea.rejected_at = None
        else:
            idea.status = "rejected"
            idea.rejected_at = timezone.now()
            idea.approved_at = None

    idea.save()
    return redirect('home')