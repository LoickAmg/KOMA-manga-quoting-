from rest_framework import serializers

from .models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    theme_label = serializers.CharField(source="get_theme_display", read_only=True)
    fr_origin_label = serializers.CharField(source="get_fr_origin_display", read_only=True)

    class Meta:
        model = Quote
        fields = [
            "id",
            "text",
            "text_fr",
            "fr_origin",
            "fr_origin_label",
            "character",
            "series",
            "source",
            "theme",
            "theme_label",
        ]
