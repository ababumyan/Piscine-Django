from django.shortcuts import render
from psycopg2 import connect ,OperationalError, DataError,ProgrammingError
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from core.service import SqlService
from .sql import ex08_planets , ex08_people
from data.service import DataService
# Create your views here.


service = SqlService()

def init(request):
    if not service.connect():
        return HttpResponse("Database connection failed", status=500)

    try:
        service.run_query('SELECT 1')  # Test the connection
        service.run_query(ex08_planets)
        service.run_query(ex08_people)
        service.close()
        return HttpResponse("ok",status=200)
    except DataError as e:
        print(f"Data error: {e}")
        return HttpResponse(f"Data error: {e}", status=500)
    except OperationalError as e:
        print(f"Operational error: {e}")
        return HttpResponse(f"Operational error: {e}", status=500)

    except Exception as e:
        print(f"Database connection failed: {e}")
        return HttpResponse(f"Database connection failed: {e}", status=500)
        


def update_table(request):
    # This function is not implemented yet, but it will be responsible for updating the ex08_planets table with data from the Star Wars API.
    try:
        conn = connect(
            host=settings.DATABASES['default']['HOST'],
            port = settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )

        conn.cursor().execute('SELECT 1')  # Test the connection
        conn.cursor().execute(""" 
                ALTER TABLE ex08_planets
                ALTER COLUMN diameter SET UNSIGNED INT,
        
            """)
        
        conn.commit()
        conn.close()
        return HttpResponse("ok",status=200)

    except DataError as e:
        print(f"Data error: {e}")
        return HttpResponse(f"Data error: {e}", status=500)
    except OperationalError as e:
        print(f"Operational error: {e}")
        return HttpResponse(f"Operational error: {e}", status=500)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return HttpResponse(f"Database connection failed: {e}", status=500)
    


def populate(self):
    try:
        if not service.connect():
            return HttpResponse("Database connection failed", status=500)
 
        data_service = DataService()
        planets_data = data_service.get_planets_data()
        people_data = data_service.get_people_data()

        for planet in planets_data:
            service.run_query(f"""
                INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
                VALUES ('{planet['name']}', '{planet['climate']}', {planet['diameter']}, {planet['orbital_period']}, {planet['population']}, {planet['rotation_period']}, {planet['surface_water']}, '{planet['terrain']}')
                ON CONFLICT (name) DO NOTHING;
            """)
        for person in people_data:
            print(person['homeworld'] == 'NULL')
            if  person['homeworld'] == 'NULL':
                print(f"Skipping {person['name']} due to missing homeworld")
                continue
            service.run_query(f"""
                INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
                VALUES ('{person['name']}', '{person['birth_year']}', '{person['gender']}', '{person['eye_color']}', '{person['hair_color']}', {person['height']}, {person['mass']}, '{person['homeworld']}')
                ON CONFLICT (name) DO NOTHING;
            """)

        service.close()
        return HttpResponse("ok",status=200)
    
    except OperationalError as e:
        print(f"Operational error: {e}")
        return HttpResponse(f"Operational error: {e}", status=500)
    except DataError as e:
        print(f"Data error: {e}")
        return HttpResponse(f"Data error: {e}", status=500)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return HttpResponse(f"Database connection failed: {e}", status=500)   




def display(request):
    try:
        if not service.connect():
            return HttpResponse("Database connection failed", status=500)


        cursor = service.conn.cursor()
        cursor.execute("""
            SELECT p.name AS planet_name, p.climate, p.diameter, p.orbital_period, p.population, p.rotation_period, p.surface_water, p.terrain,
                   pe.name AS person_name, pe.birth_year , pe.gender, pe.eye_color, pe.hair_color, pe.height, pe.mass
            FROM ex08_planets p
            LEFT JOIN ex08_people pe ON p.name = pe.homeworld
            ORDER BY p.name, pe.name;
        """)
        results = cursor.fetchall()
        cursor.close()
        service.close()
        data = []
        for row in results:
            data.append({
                "planet_name": row[0],
                "climate": row[1],
                "diameter": row[2],
                "orbital_period": row[3],
                "population": row[4],
                "rotation_period": row[5],
                "surface_water": row[6],
                "terrain": row[7],
                "person_name": row[8],
                "birth_year": row[9],
                "gender": row[10],
                "eye_color": row[11],
                "hair_color": row[12],
                "height": row[13],
                "mass": row[14]

            })
        return render(request, 'ex08/display.html', {'data': data})
    except OperationalError as e:
        print(f"Operational error: {e}")
        return HttpResponse(f"Operational error: {e}", status=500)
    except DataError as e:
        print(f"Data error: {e}")
        return HttpResponse(f"Data error: {e}", status=500)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return HttpResponse(f"Database connection failed: {e}", status=500)


