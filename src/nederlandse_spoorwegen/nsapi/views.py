from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
import requests
from dotenv import load_dotenv
import os
import json
# Create your views here.
load_dotenv()
NSAPI_KEY = os.getenv('NSAPI_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class Index(TemplateView):
    template_name = 'index.html'

    def get_stations_json(self):
        search = self.request.GET.get('q')
        if search:
            url= 'https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations'
            headers = {'Ocp-Apim-Subscription-Key': NSAPI_KEY}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response = response.json()
                for station in response['payload']:
                    if search in station['namen']['lang']:
                        return station
        else:
            return None
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['stations'] = self.get_stations_json()
            if context['stations']:
                context['lat'] = context['stations']['lat']
                context['lng'] = context['stations']['lng']
            context['googleapi'] = GOOGLE_API_KEY
            return context