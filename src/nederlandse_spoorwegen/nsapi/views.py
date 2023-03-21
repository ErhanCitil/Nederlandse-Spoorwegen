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

class NSClient:
    def __init__(self):
        self.url = 'https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/'
        self.headers = {'Ocp-Apim-Subscription-Key': NSAPI_KEY}

    def get_stations(self):
        url = self.url + 'stations'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()
            return response['payload']
        else:
            return None
        
class Index(TemplateView):
    template_name = 'nsapi/index.html'

    def get_stations_json(self):
        search = self.request.GET.get('q')
        if search:
            client = NSClient()
            stations = client.get_stations()
            for station in stations:
                if station['namen']['lang'] == search:
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
    
class StationView(TemplateView):
    template_name = 'nsapi/stations.html'

    def get_station_names(self):
        client = NSClient()
        stations = client.get_stations()
        return stations
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stations'] = self.get_station_names()
        return context

class StationDetailView(TemplateView):
    template_name = 'nsapi/station_detail.html'

    def get_station(self):
        client = NSClient()
        stations = client.get_stations()
        for station in stations:
            if station['namen']['kort'] == self.kwargs['name']:
                return station
            
    def get_departures(self):
        url = 'https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/departures?uicCode=' + str(self.get_station()['UICCode'])
        response = requests.get(url, headers={'Ocp-Apim-Subscription-Key': NSAPI_KEY})
        if response.status_code == 200:
            response = response.json()
            return response['payload']['departures']
        else:
            return None
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station'] = self.get_station()
        context['googleapi'] = GOOGLE_API_KEY
        context['departures'] = self.get_departures()
        return context