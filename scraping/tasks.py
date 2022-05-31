from background_task import background
import requests
from django.core.files.base import ContentFile

from .models import ScrapedImage


@background()
def fetch_image_and_save(scheme, domain, image_source, scrapping_url):
    if domain not in image_source:
        image_source = f'{scheme}://{domain}{image_source}'

    file_name = image_source.split('/')[-1]


    response = requests.get(image_source)

    if response.status_code == 200:
        scrapped_image_obj = ScrapedImage()
        scrapped_image_obj.image_source = image_source
        scrapped_image_obj.scraped_url = scrapping_url
        scrapped_image_obj.domain = domain

        scrapped_image_obj.image_original.save(file_name, ContentFile(response.content), save=False)
        scrapped_image_obj.save()