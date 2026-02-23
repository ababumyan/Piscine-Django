from django.shortcuts import render

# Create your views here.
from data.service import DataService
from django.http import HttpResponse, JsonResponse
from .models import Movies, Person,Planet
import json

from django.views.decorators.csrf import csrf_exempt


def display(request):
    movies = Movies.objects.all()
    if not movies.exists():
        return HttpResponse( ' No data available , please run following command:<b> python manage.py ex10_insertion </b>', status=200)
    movies_data = []
    for movie in movies:
        movies_data.append({
            'episode_nb': movie.episode_nb,
            'title': movie.title,
            'opening_crawl': movie.opening_crawl,
            'director': movie.director,
            'producer': movie.producer,
            'release_date': movie.release_date,
            'characters': [character.name for character in movie.characters.all()]
         })

    context = {
        'data': movies_data,
        'movies': movies
    }
    return render(request, 'ex10/display.html', context)


def index(request):
    return render(request, 'ex10/index.html')

@csrf_exempt
def filter_movies(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'message': 'Invalid JSON body'}, status=400)
        maximum_release_date = payload.get('maximum_release_date')
        minimum_release_date = payload.get('minimum_release_date')
        minimum_planet_diameter = payload.get('minimum_planet_diameter')
        character_gender = payload.get('character_gender')

    else:
        maximum_release_date = request.POST.get('maximum_release_date')
        minimum_release_date = request.POST.get('minimum_release_date')
        minimum_planet_diameter = request.POST.get('minimum_planet_diameter')
        character_gender = request.POST.get('character_gender')

    
    # Validate input
    if not (maximum_release_date and minimum_release_date and minimum_planet_diameter and character_gender):
        return JsonResponse({'message': 'Missing required fields'}, status=400)

    # Filter persons by gender
    persons = Person.objects.filter(gender=character_gender, homeworld__diameter__gte=minimum_planet_diameter)
    results = []
    for person in persons:
        # Filter movies for this person
        movies = person.movies_set.filter(
            release_date__gte=minimum_release_date,
            release_date__lte=maximum_release_date
        )
        for movie in movies:
            results.append({
                'film_title': movie.title,
                'character_name': person.name,
                'gender': person.gender,
                'homeworld_name': person.homeworld.name if person.homeworld else '',
                'homeworld_diameter': person.homeworld.diameter if person.homeworld else ''
            })
    if not results:
        return JsonResponse({'message': 'Nothing corresponding to your research'}, status=200)
    return JsonResponse(results, safe=False)