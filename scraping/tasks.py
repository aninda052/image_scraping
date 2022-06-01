
from background_task import background
import requests
from django.core.files.base import ContentFile
from multiprocessing import Pool, cpu_count
from .models import ScrapedImage
import validators

@background()
def fetch_image_and_save(image_source_list, scheme, domain, scrapping_url):

    fetch_image_function_arg_list = []
    for image_source in image_source_list:

        # if domain not in image_source:
        #     image_source = f'{scheme}://{domain}{image_source}'

        if not ScrapedImage.objects.filter(image_source=image_source).exists():
            file_name = f"{image_source.split('/')[-1].split('.')[0]}.jpeg"

            fetch_image_function_arg_list.append([image_source, scrapping_url, domain, file_name])


    pool = Pool(processes=cpu_count()-1)
    pool.map(fetch_image_wrapper, fetch_image_function_arg_list)



def fetch_image_wrapper(args):
    fetch_image(*args)

def fetch_image(image_source, scrapping_url, domain, file_name):

    if validators.url(image_source):
        response =  requests.get(image_source)
        if response.status_code == 200:
            scrapped_image_obj = ScrapedImage()
            scrapped_image_obj.image_source = image_source
            scrapped_image_obj.scraped_url = scrapping_url
            scrapped_image_obj.domain = domain

            scrapped_image_obj.image_original.save(file_name, ContentFile(response.content), save=False)
            scrapped_image_obj.save()

