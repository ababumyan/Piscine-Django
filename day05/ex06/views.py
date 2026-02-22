import json

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
        conn.cursor().execute("""CREATE TABLE IF NOT EXISTS ex06_movies 
                            (episode_nb SERIAL PRIMARY KEY, 
                              title VARCHAR(64) UNIQUE NOT NULL, 
                              opening_crawl TEXT, 
                              director VARCHAR(64) NOT NULL, 
                              producer VARCHAR(128) NOT NULL, 
                              release_date DATE NOT NULL,
                              created TIMESTAMP DEFAULT NOW(),
                              updated TIMESTAMP DEFAULT NOW() );""")
        conn.cursor().execute("""CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                                RETURNS TRIGGER AS $$
                                BEGIN
                                    NEW.updated = now();
                                    NEW.created = OLD.created;
                                    RETURN NEW;
                                END;
                                $$ language 'plpgsql';
                                """)

        conn.cursor().execute("""DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
                                CREATE TRIGGER update_films_changetimestamp
                                BEFORE UPDATE ON ex06_movies
                                FOR EACH ROW
                                EXECUTE PROCEDURE update_changetimestamp_column();
                                """)
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
            conn.cursor().execute("""INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date) 
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
        cursor.execute("SELECT * FROM ex06_movies;")
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

    return render(request, 'ex06/display.html', {'movies': movies})


def update_view(request):
    movies_data = get_movies()
    if  isinstance(movies_data, HttpResponse) and movies_data.status_code != 200:
        return HttpResponse('No data available', status=404)
    return render(request, 'ex06/update.html', {'movies': movies_data})


def update_by_opening_crawl(request, title):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
    movies_data = get_movies()
    opening_crawl = None
    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'message': 'Invalid JSON body'}, status=400)
        opening_crawl = payload.get('opening_crawl')
    else:
        opening_crawl = request.POST.get('opening_crawl')

    print(f"Received opening_crawl: '{opening_crawl}' for title: '{title}'")
    if not opening_crawl:
        return JsonResponse({'message': 'Opening crawl is required'}, status=400)
    if  isinstance(movies_data, HttpResponse) and movies_data.status_code != 200:
        return JsonResponse({'message': 'No data available'}, status=404)
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
        cursor.execute("UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;", (opening_crawl, title))
        if cursor.rowcount == 0:
            conn.close()
            return JsonResponse({'message': 'Movie not found'}, status=404)
        conn.commit()
        conn.close()
        return JsonResponse({'message': 'Movie updated successfully'}, status=200)
    except OperationalError as e:
        return JsonResponse({'message': f'OperationalError: {e}'}, status=500)
    except DataError as e:
        return JsonResponse({'message': f'DataError: {e}'}, status=500)
    except Exception as e:
        return JsonResponse({'message': f'Error: {e}'}, status=500)
