
from background_task import background
import requests
from django.core.files.base import ContentFile
from multiprocessing import Pool, cpu_count
from .models import ScrapedImage
import validators



@background()
def fetch_image_and_save(image_source_list, scheme, domain, scrapping_url):
    """
        This function will run in background
        Will filter out all the existing images and
        Invoke multiple worker processor for fetching rest of the image
    """

    # this list will append all the image source which are not already in database
    fetch_image_function_arg_list = []

    # loop through over each image source
    for image_source in image_source_list:

        # checking if this image (image source) already exist or not
        if not ScrapedImage.objects.filter(image_source=image_source).exists():
            '''if not exist, we'll try to fetch this image '''

            # extracting file name for this image by splitting image source
            file_name = f"{image_source.split('/')[-1]}"

            fetch_image_function_arg_list.append([image_source, scrapping_url, domain, file_name])

    # assigning worker processor
    pool = Pool(processes=cpu_count()-1)

    # parallelly fetching images
    pool.starmap(fetch_image, fetch_image_function_arg_list)




def fetch_image(image_source, scrapping_url, domain, file_name):
    """
        Pull image for a given url and
        Store the image information in database
    """

    # checking image source is valid or not
    if validators.url(image_source):
        response =  requests.get(image_source)

        # checking if the image  pulling successful or not
        if response.status_code == 200:
            scrapped_image_obj = ScrapedImage()
            scrapped_image_obj.image_source = image_source
            scrapped_image_obj.scraped_url = scrapping_url
            scrapped_image_obj.domain = domain

            # storing source image as file in media directory, this won't make any database call
            scrapped_image_obj.image_original.save(file_name, ContentFile(response.content), save=False)

            # storing image path with other metadata in database using custom save() method
            # We override save() method for ScrapedImage model, this custom method can be found in ScrapedImage model
            scrapped_image_obj.save()

