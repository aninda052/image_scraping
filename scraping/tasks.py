from background_task import background
import requests
from django.core.files.base import ContentFile

from .models import ScrapedImage


@background()
def fetch_image_and_save(image_source_list, scheme, domain, scrapping_url):

    for image_source in image_source_list:

        if domain not in image_source:
            image_source = f'{scheme}://{domain}{image_source}'

        if not ScrapedImage.objects.filter(image_source=image_source).exists():
            file_name = f"{image_source.split('/')[-1].split('.')[0]}.jpeg"
            try:
                response = requests.get(image_source)

                if response.status_code == 200:
                    scrapped_image_obj = ScrapedImage()
                    scrapped_image_obj.image_source = image_source
                    scrapped_image_obj.scraped_url = scrapping_url
                    scrapped_image_obj.domain = domain

                    scrapped_image_obj.image_original.save(file_name, ContentFile(response.content), save=False)
                    scrapped_image_obj.save()
            except:
                pass