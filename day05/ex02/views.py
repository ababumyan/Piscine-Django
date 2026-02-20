from psycopg2 import connect, OperationalError,DataError
from django.conf import settings
from django.http import  HttpResponse
from django.shortcuts import render
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
        conn.cursor().execute("""CREATE TABLE IF NOT EXISTS ex02_movies
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
        movies = [
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
        for movie in movies:
            conn.cursor().execute("""INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date) 
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
    

def display(request):
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
        cursor.execute("SELECT * FROM ex02_movies;")
        movies = cursor.fetchall()
        conn.close()
        if not movies:
            return HttpResponse('No data available')
        return render(request, 'ex02/display.html', {'movies': movies})
    except OperationalError as e:
        return HttpResponse(f'OperationalError: {e}', status=500)
    except DataError as e:
        return HttpResponse(f'DataError: {e}', status=500)
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)