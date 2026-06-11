from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json

from .models import Idea, Comment
from .serializer import CommentSerializer, IdeaSerializer

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"csrf": "ok"})
    
@ensure_csrf_cookie
@csrf_exempt
def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthenticated"}, status=401)

    return JsonResponse({
        "username": request.user.username,
        "is_superuser": request.user.is_superuser
    })


@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)

    data = json.loads(request.body.decode("utf-8") or "{}")

    user = authenticate(
        username=data.get("username"),
        password=data.get("password")
    )

    if not user:
        return JsonResponse({"error": "invalid credentials"}, status=401)

    login(request, user)

    return JsonResponse({"ok": True})


@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({"ok": True})

class IdeaListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ideas = Idea.objects.all().order_by('-created_at')
        return Response(IdeaSerializer(ideas, many=True).data)

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")

        if not title or not description:
            return Response({"error": "Missing fields"}, status=400)

        idea = Idea.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return Response(IdeaSerializer(idea).data, status=201)

class SetStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, idea_id, status_type):
        idea = get_object_or_404(Idea, id=idea_id)

        if not request.user.is_superuser:
            return Response({"error": "forbidden"}, status=403)

        if status_type == "approved":
            idea.status = "approved"
            idea.approved_at = timezone.now()

        elif status_type == "rejected":
            idea.status = "rejected"
            idea.rejected_at = timezone.now()

        idea.save()
        return Response({"status": "ok"})

@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id)
        comments = Comment.objects.filter(idea=idea).order_by("-created_at")

        return Response(CommentSerializer(comments, many=True).data)

    def post(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id)

        serializer = CommentSerializer(
            data=request.data,
            context={"request": request, "view": self}
        )

        if serializer.is_valid():
            serializer.save(user=request.user, idea=idea)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


        