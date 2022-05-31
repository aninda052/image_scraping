
from django.urls import path
from scraping.api.scraping_api_view import ImageListAPI

app_name= 'scraping_api'

urlpatterns = [
    path('get-image', ImageListAPI.as_view(), name='get_image_api'),
]