from rest_framework import serializers
from scraping.models import ScrapedImage

class ImageListSerializer(serializers.ModelSerializer):
    image_id = serializers.IntegerField(source="id")
    class Meta:
        model = ScrapedImage
        fields = [
            "image_id",
            "image_source",
            "scraped_url",
            "domain",
            "image_dimension",
            "download_date",
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = instance.image_original.url
        return data
