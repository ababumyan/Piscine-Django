from django.shortcuts import render
from .models import Movies
from django.http import HttpResponse ,JsonResponse
import json
# Create your views here.
def populate(request):
    movies_data = [
            {
                "episode_nb": 1,
                "title": "The Phantom Menace",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "1999-05-19"
            },
            {
                "episode_nb": 2,
                "title": "Attack of the Clones",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2002-05-16"
            },
            {
                "episode_nb": 3,
                "title": "Revenge of the Sith",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2005-05-19"
            },
            {
                "episode_nb": 4,
                "title": "A New Hope",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25"
            },
            {
                "episode_nb": 5,
                "title": "The Empire Strikes Back",
                "director": "Irvin Kershner",
                "producer": "Gary Kutz, Rick McCallum",
                "release_date": "1980-05-17"
            },
            {
                "episode_nb": 6,
                "title": "Return of the Jedi",
                "director": "Richard Marquand",
                "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
                "release_date": "1983-05-25"
            },
            {
                "episode_nb": 7,
                "title": "The Force Awakens",
                "director": "J.J. Abrams",
                "producer": "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
                "release_date": "2015-12-11"
            },
            {
                "episode_nb": 8,
                "title": "The Last Jedi",
                "director": "Rian Johnson",
                "producer": "Kathleen Kennedy, Ram Bergman",
                "release_date": "2017-12-13"
            },
            {
                "episode_nb": 9,
                "title": "The Rise of Skywalker",
                "director": "J.J. Abrams",
                "producer": "Kathleen Kennedy, J.J. Abrams, Michelle Rejwan",
                "release_date": "2019-12-18"
            },
        ]
    try:
        get_movies = []
        for movie in movies_data:
            get, created = Movies.objects.get_or_create(
                episode_nb=movie["episode_nb"],
                title=movie["title"],
                director=movie["director"],
                producer=movie["producer"],
                release_date=movie["release_date"]
                )
            if not created:
                get_movies.append(f'<br>{movie["title"]} already exists')
        if get_movies:
            return HttpResponse(f'Movies already exist: {", ".join(get_movies)}')

    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    
    return HttpResponse('ok')

def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse('No data available')
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    return render(request, 'ex05/display.html', {'movies': movies})


def update_view(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse('No data available')
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    return render(request, 'ex07/update.html', {'movies': movies})

def update_by_title_opening_crawl(request, title):
    if request.method != 'POST':
        return JsonResponse('Method not allowed', status=405)
    try:
        movie = Movies.objects.filter(title=title).first()
        if not movie:
            print(f'Movie "{title}" not found.')
            return JsonResponse('Movie not found', status=404)
        data = json.loads(request.body)
        if 'opening_crawl' not in data:
            return JsonResponse('Missing opening_crawl in request body', status=400)
        movie.update_opening_crawl(data['opening_crawl'])
        print(f'Movie "{title}" updated successfully.')
        return JsonResponse({'message': 'Movie updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse(f'Error: {e}', status=500)