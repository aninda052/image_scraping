from django.urls import path

from scraping.views import LandingPageView

app_name = 'scraping'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page_url'),

]