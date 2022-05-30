from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


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

            image_url_list = []
            for item in soup.find_all('img'):
                image_source = ""
                if 'src' in item.attrs:
                    image_source = item['src']
                if image_source:
                    if domain not in image_source:
                        image_source = f'{scheme}://{domain}{image_source}'
                    image_url_list.append(image_source)

            massage = f'Total {len(image_url_list)} images found'

        context = {"massage" : massage}
        return render(request, 'landing.html', context=context)




