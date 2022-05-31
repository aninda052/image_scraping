from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from scraping.models import ScrapedImage


class ImageListAPI(generics.ListAPIView):
    queryset = ScrapedImage.objects.all()
    paginate_by = 10

    def filter_queryset(self):
        image_id = int(self.request.query_params.get("image_id", 0))
        image_source = self.request.query_params.get("image_source", "")
        image_size = self.request.query_params.get("image_size", "")
        scraped_url = self.request.query_params.get("scraped_url", "")

        filter  = {}

        if image_id:
            filter["id"] = image_id

        if image_source:
            filter["image_source"] = image_source

        if scraped_url:
            filter["scraped_url"] = scraped_url

        queryset = self.queryset.filter(**filter)

        return queryset



    def get(self, request):
        base_url = f"{self.request.scheme}://{self.request.get_host()}"

        if not self.filter_queryset().count():
            return Response({"massage": "No image Found"}, status=status.HTTP_404_NOT_FOUND)
        data = [
            {
                "image_id" : image.id,
                "image_url": f'{base_url}{image.image.url}',
                "image_source": image.image_source,
                "scraped_url": image.scraped_url,
                "domain": image.domain,
                "download_date": image.download_date,
            }
            for image in self.filter_queryset()
        ]

        return Response({"data": data}, status=status.HTTP_200_OK)