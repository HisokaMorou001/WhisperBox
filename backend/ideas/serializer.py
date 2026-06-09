from rest_framework import serializers
from .models import Comment, Idea

class CommentSerializer(serializers.ModelSerializer):
    # Campi utili per il frontend presi direttamente dall'utente collegato
    username = serializers.ReadOnlyField(source='user.username')
    is_admin = serializers.ReadOnlyField(source='user.is_superuser')

    class Meta:
        model = Comment
        fields = ["id", "text", "created_at", "username", "is_admin"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        # Spostiamo qui la logica di business del commento unico!
        request = self.context.get('request')
        idea_id = self.context.get('view').kwargs.get('idea_id')
        
        if request and request.user:
            if Comment.objects.filter(idea_id=idea_id, user=request.user).exists():
                raise serializers.ValidationError("Hai già commentato questa idea.")
        return attrs


class IdeaSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Idea
        fields = ["id", "title", "description", "status", "created_at", "username"]