from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

# Import per DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Idea, Comment
from .serializer import CommentSerializer

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
def set_status(request, idea_id, status_type):
    idea = get_object_or_404(Idea, id=idea_id)

    if status_type == "approved":
        if idea.status == "approved":
            idea.status = "pending"
            idea.approved_at = None
        else:
            idea.status = "approved"
            idea.approved_at = timezone.now()
            idea.rejected_at = None

    elif status_type == "rejected":
        if idea.status == "rejected":
            idea.status = "pending"
            idea.rejected_at = None
        else:
            idea.status = "rejected"
            idea.rejected_at = timezone.now()
            idea.approved_at = None

    idea.save()
    return redirect('home')

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] # Sostituisce @login_required

    def get(self, request, idea_id):
        """Sostituisce get_comments"""
        idea = get_object_or_404(Idea, id=idea_id)
        comments = Comment.objects.filter(idea=idea).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, idea_id):
        """Sostituisce add_comment"""
        idea = get_object_or_404(Idea, id=idea_id)
        
        # Passiamo il contesto alla validazione del serializer
        serializer = CommentSerializer(data=request.data, context={'request': request, 'view': self})
        
        if serializer.is_valid():
            # Salviamo iniettando l'utente e l'idea correnti
            serializer.save(user=request.user, idea=idea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)