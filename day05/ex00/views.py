from django.shortcuts import render
from psycopg2 import connect, OperationalError,DataError
from django.conf import settings
from django.http import JsonResponse, HttpResponse




# Create your views here.
def index(request):
    try:
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        conn.cursor().execute('SELECT 1')  # Test the connection
        conn.cursor().execute("""CREATE TABLE IF NOT EXISTS ex00_movies 
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