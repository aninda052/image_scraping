from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from scraping.models import ScrapedImage
from scraping.serializer.scraping_serializer import ImageListSerializer


class ImageListAPI(generics.ListAPIView):
    queryset = ScrapedImage.objects.all()
    serializer_class = ImageListSerializer

    def get_queryset(self):
        image_id = int(self.request.query_params.get("image_id", 0))
        image_source = self.request.query_params.get("image_source", "")
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

        image_id = int(self.request.query_params.get("image_id", 0))
        image_source = self.request.query_params.get("image_source", "")

        if image_id and image_source:
            return Response({"massage": "You can either use image_id or image_source"}, status=status.HTTP_409_CONFLICT)

        if not self.get_queryset().count():
            return Response({"massage": "No image Found"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(self.get_queryset())

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'image_size': request.query_params.get("image_size", "")})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(),many=True, context={'image_size': request.query_params.get("image_size", "")})
        return Response(serializer.data)