from rest_framework import serializers
from .models import Comment, Idea


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    is_admin = serializers.ReadOnlyField(source='user.is_superuser')

    class Meta:
        model = Comment
        fields = ["id", "text", "created_at", "username", "is_admin"]
        read_only_fields = ["id", "created_at"]

    def validate_text(self, attrs):
        request = self.context.get("request")
        view = self.context.get("view")

        idea_id = getattr(view, "kwargs", {}).get("idea_id")

        if request and request.user and idea_id:
            exists = Comment.objects.filter(
                idea_id=idea_id,
                user=request.user
            ).exists()

            if exists:
                raise serializers.ValidationError(
                    "Hai già commentato questa idea."
                )

        return attrs