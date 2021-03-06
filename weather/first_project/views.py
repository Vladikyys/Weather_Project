from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = 'ec0dbd7b1ddd596a656aaaeee7389f62'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cities = City.objects.all()
    print(cities)
    if len(cities) == 1:
        City.objects.all().delete()
        redirect('weather/index.html')
    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)

