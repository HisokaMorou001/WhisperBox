from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from ideas.views import csrf

from ideas.views import (
    IdeaListCreateAPIView,
    SetStatusAPIView,
    CommentListCreateAPIView,
    api_login,
    api_logout,
    api_me,
    csrf
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", RedirectView.as_view(url="http://localhost:3000/", permanent=False)),


    path("api/auth/login/", api_login),
    path("api/auth/logout/", api_logout),
    path("api/auth/me/", api_me),

    path("api/ideas/", IdeaListCreateAPIView.as_view()),
    path("api/auth/csrf/", csrf),
    path("api/status/<int:idea_id>/<str:status_type>/", SetStatusAPIView.as_view()),

    path("api/ideas/<int:idea_id>/comments/", CommentListCreateAPIView.as_view()),
]