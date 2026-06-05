from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST

from .models import Idea, Comment


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

@login_required
def get_comments(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    comments = Comment.objects.filter(idea=idea).order_by("-created_at")

    data = [
        {
            "id": c.id,
            "text": c.text,
            "created_at": c.created_at
        }
        for c in comments
    ]

    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def add_comment(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    # 1 solo commento per utente per idea
    if Comment.objects.filter(idea=idea, user=request.user).exists():
        return JsonResponse(
            {"error": "Hai già commentato questa idea"},
            status=400
        )

    try:
        body = json.loads(request.body)
        text = body.get("text", "")
    except:
        return JsonResponse({"error": "Dati non validi"}, status=400)

    comment = Comment.objects.create(
        idea=idea,
        user=request.user,
        text=text
    )

    return JsonResponse({
        "id": comment.id,
        "text": comment.text,
        "created_at": comment.created_at
    })

    