from django.shortcuts import render

# Create your views here.
from data.service import DataService
from django.http import HttpResponse, JsonResponse
from .models import Movies, Person,Planet
import json
from datetime import datetime

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
    return JsonResponse({
        'data': json.loads(json.dumps(movies_data, default=str)),
        'movies': json.loads(json.dumps(list(movies.values()), default=str))  # Convert date objects to strings
    }, safe=False)
    return render(request, 'ex10/display.html', context)


def index(request):
    return render(request, 'ex10/index.html')

@csrf_exempt
def get_genders(request):
    """Fetch all unique genders from the Person model"""
    genders = Person.objects.values_list('gender', flat=True).distinct().order_by('gender')
    return JsonResponse(list(genders), safe=False)

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

    # Convert date strings to date objects
    try:
        min_date = datetime.strptime(minimum_release_date, '%Y-%m-%d').date()
        max_date = datetime.strptime(maximum_release_date, '%Y-%m-%d').date()
        min_diameter = int(minimum_planet_diameter)
    except ValueError as e:
        return JsonResponse({'message': f'Invalid input format: {str(e)}'}, status=400)

    print(f"DEBUG: Searching for gender={character_gender}, min_diameter={min_diameter}, date range: {min_date} to {max_date}")
    
    # Debug: check what genders exist
    all_genders = Person.objects.values_list('gender', flat=True).distinct()
    print(f"DEBUG: Available genders in DB: {list(all_genders)}")
    
    # Debug: check all persons with this gender
    all_with_gender = Person.objects.filter(gender=character_gender)
    print(f"DEBUG: Total persons with gender={character_gender}: {all_with_gender.count()}")
    
    # Debug: check how many have homeworld
    with_homeworld = all_with_gender.filter(homeworld__isnull=False)
    print(f"DEBUG: Persons with gender={character_gender} AND homeworld: {with_homeworld.count()}")
    
    # Debug: show all with this gender and their homeworld
    for p in all_with_gender[:5]:
        print(f"  - {p.name}: homeworld={p.homeworld}, diameter={p.homeworld.diameter if p.homeworld else 'NULL'}")
    
    # Filter persons by gender and homeworld diameter
    persons = Person.objects.filter(
        gender=character_gender, 
        homeworld__isnull=False
    ).filter(homeworld__diameter__gte=min_diameter)
    
    print(f"DEBUG: After all filters: {persons.count()} persons")
    
    # Debug: print all persons with their homeworld diameters
    for p in persons:
        print(f"  - {p.name}: homeworld={p.homeworld.name if p.homeworld else 'None'}, diameter={p.homeworld.diameter if p.homeworld else 'None'}")
    
    results = []
    for person in persons:
        # Filter movies for this person using the many-to-many relationship
        movies = Movies.objects.filter(
            characters=person,
            release_date__gte=min_date,
            release_date__lte=max_date
        )
        print(f"DEBUG: Found {movies.count()} movies for {person.name} between {min_date} and {max_date}")
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