from django.urls import path

from scrapping.views import LandingPageView

app_name = 'scrapping'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page_url'),

]