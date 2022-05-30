
from django.urls import path
from scraping.api.scraping import GetImageAPI

app_name= 'scraping_api'

urlpatterns = [
    path('get-image', GetImageAPI.as_view(), name='get_image_api'),
]