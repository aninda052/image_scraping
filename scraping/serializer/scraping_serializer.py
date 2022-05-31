from rest_framework import serializers
from scraping.models import ScrapedImage

class ImageListSerializer(serializers.ModelSerializer):
    image_id = serializers.IntegerField(source="id")
    class Meta:
        model = ScrapedImage
        fields = [
            "image_id",
            "image",
            "image_source",
            "scraped_url",
            "domain",
            "image_dimension",
            "download_date",
        ]
