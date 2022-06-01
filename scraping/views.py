from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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


            image_source_list = list(set(item['src'] for item in soup.find_all('img')
                                 if 'src' in item.attrs and item['src']  and 'svg' not in item['src'].split('.')[-1]))

            fetch_image_and_save.now(image_source_list, scheme, domain, scrapping_url)

            massage = f'Total {len(image_source_list)} images source found'

        context = {"massage" : massage}
        return render(request, 'landing.html', context=context)




