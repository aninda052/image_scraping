from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import validators
from .tasks import fetch_image_and_save

class LandingPageView(View):

    def get(self, request):
        return render(request, 'landing.html')

    def post(self, request):
        scrapping_url = request.POST.get("scrappingUrl", "")

        # validating url
        if not validators.url(scrapping_url):
            massage = "Please provide a valid url"
        else:
            # Pulling html page of the given url
            response = requests.get(scrapping_url)

            # checking if pulling is successful or not
            if response.status_code == 200:

                # extract domain and scheme from url
                url_parser = urlparse(scrapping_url)
                domain = url_parser.netloc
                scheme = url_parser.scheme

                htmldata = response.text

                # creating soup object for extracting data programmatically
                soup = BeautifulSoup(htmldata, 'html.parser')

                # making list of unique image source while filtering out any svg image
                image_source_list = list(set(item['src'] for item in soup.find_all('img')
                                     if 'src' in item.attrs and item['src']  and 'svg' not in item['src'].split('.')[-1]))

                # extracting image from image source using background task
                fetch_image_and_save(image_source_list, scheme, domain, scrapping_url)

                massage = f'Total {len(image_source_list)} images source found'

            else:
                massage = f"Couldn't pull data from given url, url return with {response.status_code} status"

        context = {"massage" : massage}
        return render(request, 'landing.html', context=context)




