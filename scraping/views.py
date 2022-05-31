from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .models import ScrapedImage
from .tasks import fetch_image_and_save

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

                if not image_source or 'svg' in image_source.split('.')[-1]:
                    continue
                if not ScrapedImage.objects.filter(image_source=image_source).exists():
                    fetch_image_and_save(scheme, domain,image_source, scrapping_url)
                    scrapped_image_count += 1

            massage = f'Total {scrapped_image_count} images found'

        context = {"massage" : massage}
        return render(request, 'landing.html', context=context)




