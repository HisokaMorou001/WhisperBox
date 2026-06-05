from django.contrib import admin
from django.utils import timezone
from .models import Idea
from .models import Comment


@admin.action(description="Approve selected ideas")
def approve_ideas(modeladmin, request, queryset):
    queryset.update(
        status="approved",
        approved_at=timezone.now(),
        rejected_at=None
    )


@admin.action(description="Reject selected ideas")
def reject_ideas(modeladmin, request, queryset):
    queryset.update(
        status="rejected",
        rejected_at=timezone.now(),
        approved_at=None
    )


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at", "approved_at", "rejected_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")

    actions = [approve_ideas, reject_ideas]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "idea", "text", "created_at")
    search_fields = ("text", "user__username", "idea__title")
    list_filter = ("created_at", "idea")