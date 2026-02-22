from django.shortcuts import render
from psycopg2 import connect, OperationalError,DataError
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ex02.views import movies

# Create your views here.
def init(request):
    try:
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        conn.cursor().execute('SELECT 1')  # Test the connection
        conn.cursor().execute("""CREATE TABLE IF NOT EXISTS ex04_movies 
                            (episode_nb SERIAL PRIMARY KEY, 
                              title VARCHAR(64) UNIQUE NOT NULL, 
                              opening_crawl TEXT, 
                              director VARCHAR(64) NOT NULL, 
                              producer VARCHAR(128) NOT NULL, 
                              release_date DATE NOT NULL );""")
        conn.commit()
        conn.close()
        return HttpResponse('ok')
    except OperationalError as e:
        return HttpResponse(f'OperationalError: {e}', status=500)
    except DataError as e:
        return HttpResponse(f'DataError: {e}', status=500)
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    

def populate(request):
    try:
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        conn.cursor().execute('SELECT 1')  # Test the connection
        for movie in movies:
            conn.cursor().execute("""INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date) 
                                    VALUES (%s, %s, %s, %s, %s) 
                                    ON CONFLICT (episode_nb) DO NOTHING;""", (
                                        movie["episode_nb"],
                                        movie["title"],
                                        movie["director"],
                                        movie["producer"],
                                        movie["release_date"]
                                    ))
        conn.commit()
        conn.close()
        return HttpResponse('ok')
    except OperationalError as e:
        return HttpResponse(f'OperationalError: {e}', status=500)
    except DataError as e:
        return HttpResponse(f'DataError: {e}', status=500)
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)

def get_movies():
    try:
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        conn.cursor().execute('SELECT 1')  # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ex04_movies;")
        movies = cursor.fetchall()
        conn.close()
        print(f"Movies fetched: {movies}")
        if not movies:
            print("No movies found in the database.")
            return HttpResponse('No data available', status=404)
        return movies
    except OperationalError as e:
        return HttpResponse(f'OperationalError: {e}', status=500)
    except DataError as e:
        return HttpResponse(f'DataError: {e}', status=500)
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)

def display(request):
    movies = get_movies()
    if  isinstance(movies, HttpResponse) and movies.status_code != 200:
        return HttpResponse('No data available', status=404)

    return render(request, 'ex04/display.html', {'movies': movies})
    
def remove_view(request):
    movies = get_movies()
 
    if  isinstance(movies, HttpResponse) and movies.status_code != 200:
        return HttpResponse('No data available', status=404)
    return render(request, 'ex04/remove.html', {'movies': movies})


def remove_by_title(request, title):
    try:
        print(f"Title to remove: {title}")
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute('SELECT 1')  # Test the connection
        cursor.execute("""DELETE FROM ex04_movies WHERE title = %s;""", (title,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        if deleted == 0:
            print(f'Movie "{title}" not found.')
            return HttpResponse('Movie not found', status=404)
        print(f'Movie "{title}" removed successfully.')
        return HttpResponse('ok', status=200)
    except OperationalError as e:
        return JsonResponse({'success': False, 'error': f'OperationalError: {e}'}, status=500)
    except DataError as e:
        return JsonResponse({'success': False, 'error': f'DataError: {e}'}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {e}'}, status=500)
