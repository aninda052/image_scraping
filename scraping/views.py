from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.db import IntegrityError

from scraping.models import ScrappedImage


class LandingPageView(View):

    def get(self, request):
        return render(request, 'landing.html')

    def post(self, request):
        scrapping_url = request.POST.get("scrappingUrl", "")
        if not scrapping_url:
            massage = "Please provide a vali url"
        else:

            url_parser = urlparse(scrapping_url)
            domain = url_parser.netloc
            scheme = url_parser.scheme

            htmldata = requests.get(scrapping_url).text
            soup = BeautifulSoup(htmldata, 'html.parser')

            scrapped_image_count = 0
            for item in soup.find_all('img'):
                image_source = ""
                if 'src' in item.attrs:
                    image_source = item['src']
                if image_source:
                    if domain not in image_source:
                        image_source = f'{scheme}://{domain}{image_source}'
                        file_name = image_source.split('/')[-1]

                    response = requests.get(image_source)
                    if response.status_code == 200:
                        scrapped_image_obj = ScrappedImage()
                        scrapped_image_obj.image_source = image_source
                        scrapped_image_obj.scraped_url = scrapping_url
                        scrapped_image_obj.domain = domain
                        try:
                            scrapped_image_obj.image.save(file_name,ContentFile(response.content))
                            scrapped_image_count += 1
                        except IntegrityError: # image_source already exist in db
                            pass




            massage = f'Total {scrapped_image_count} images found'

        context = {"massage" : massage}
        return render(request, 'landing.html', context=context)




