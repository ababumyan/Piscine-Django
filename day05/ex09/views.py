from django.shortcuts import render
from .models import Planet, Person
from django.http import HttpResponse,JsonResponse
from data.service import DataService

service = DataService()
# Create your views here.
def display(request):

    planets = Planet.objects.all()
    people = Person.objects.all()
    if not planets.exists() or not people.exists():
        return HttpResponse( ' No data available , please run following command:<b> python manage.py ex09_insertion </b>', status=200)
    people_data = []
    for person in people:
        people_data.append({
            'name': person.name,
            'birth_year': person.birth_year,
            'gender': person.gender,
            'eye_color': person.eye_color,
            'hair_color': person.hair_color,
            'height': person.height,
            'homeworld': person.homeworld.name if person.homeworld else 'Unknown',
            'climate': person.homeworld.climate if person.homeworld else 'Unknown',
            'diameter': person.homeworld.diameter if person.homeworld else 'Unknown',
            'orbital_period': person.homeworld.orbital_period if person.homeworld else 'Unknown',
            'population': person.homeworld.population if person.homeworld else 'Unknown',
            'rotation_period': person.homeworld.rotation_period if person.homeworld else 'Unknown',
            'surface_water': person.homeworld.surface_water if person.homeworld else 'Unknown',
            'terrain': person.homeworld.terrain if person.homeworld else 'Unknown'
         })

    context = {
        'data': people_data,
        'people': people
    }
    return render(request, 'ex09/display.html', context)



def insert_data(request):
        service = DataService()
        data = service.get_initial_data()
        people_data = []
        Planet_data = []
        def find_planet(num):
             for item in Planet_data:
                  if item['pk'] == num:
                       return item['name']
             return None
             
        for item in data:
            if item['model'] == 'ex09.planets':
                Planet_data.append({
                    'name': item['fields']['name'],
                    'climate': item['fields']['climate'],
                    'diameter': item['fields']['diameter'],
                    'orbital_period': item['fields']['orbital_period'],
                    'population': item['fields']['population'],
                    'rotation_period': item['fields']['rotation_period'],
                    'surface_water': item['fields']['surface_water'],
                    'terrain': item['fields']['terrain'],
                    'pk': item['pk']
                })
            elif item['model'] == 'ex09.people':
                people_data.append({
                    'name': item['fields']['name'],
                    'birth_year': item['fields']['birth_year'],
                    'eye_color': item['fields']['eye_color'],
                    'gender': item['fields']['gender'],
                    'hair_color': item['fields']['hair_color'],
                    'height': item['fields']['height'],
                    'mass': item['fields']['mass'],
                    'homeworld': find_planet(item['fields']['homeworld']),
                    'pk': item['pk']
                })
        return JsonResponse({
            'planets': Planet_data,
            'people': people_data
        }, safe=False)