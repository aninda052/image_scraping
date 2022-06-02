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
            "download_date",
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        image_size = request.query_params.get("image_size", "")


        # assigning original image url as default image
        image_url = instance.image_original.url

        # assigning original image dimension as default dimension
        image_dimension = f'{instance.image_original.width}*{instance.image_original.height}'

        if image_size == "small" and instance.image_small:
            image_url = instance.image_small.url
            image_dimension = f'{instance.image_small.width}*{instance.image_small.height}'

        elif image_size == "medium" and instance.image_medium:
            image_url = instance.image_medium.url
            image_dimension = f'{instance.image_medium.width}*{instance.image_medium.height}'

        elif image_size == "large" and instance.image_large:
            image_url = instance.image_large.url
            image_dimension = f'{instance.image_large.width}*{instance.image_large.height}'

        data["image"] = request.build_absolute_uri(image_url)
        data["image_dimension"] = image_dimension
        return data
