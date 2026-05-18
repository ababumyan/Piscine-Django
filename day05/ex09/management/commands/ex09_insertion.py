from django.core.management.base import BaseCommand
from data.service import DataService
from ex09.models import Planet, Person

class Command(BaseCommand):
    help = 'Inserts data into the Planet and Person models from the Star Wars API'

    def handle(self, *args, **kwargs):
        service = DataService()
        data = service.get_initial_data()
        people_data = []
        Planet_data = []
        def find_planet(num):
             if num is None:
                    return None
             for item in Planet_data:
                  if item['pk'] == num:
                       print(f"Found planet: {item['name']} for pk: {num}")
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
                    'pk': item['pk']  # keep pk for lookup only
                })

        # Only use model fields for bulk_create, create model instances
        Planet.objects.bulk_create([
            Planet(
                name=planet['name'],
                climate=planet['climate'],
                diameter=planet['diameter'],
                orbital_period=planet['orbital_period'],
                population=planet['population'],
                rotation_period=planet['rotation_period'],
                surface_water=planet['surface_water'],
                terrain=planet['terrain']
            ) for planet in Planet_data
        ],ignore_conflicts=True)  # ignore_conflicts to skip duplicates based on unique constraints

        for item in data:
            if item['model'] == 'ex09.people':
                people_data.append({
                    'name': item['fields']['name'],
                    'birth_year': item['fields']['birth_year'],
                    'eye_color': item['fields']['eye_color'],
                    'gender': item['fields']['gender'],
                    'hair_color': item['fields']['hair_color'],
                    'height': item['fields']['height'],
                    'mass': item['fields']['mass'],
                    'homeworld': Planet.objects.get(name=find_planet(item['fields']['homeworld'])) if find_planet(item['fields']['homeworld']) else None,
                    'pk': item['pk']  # keep pk for lookup only
                })

        Person.objects.bulk_create([
            Person(
                name=person['name'],
                birth_year=person['birth_year'],
                eye_color=person['eye_color'],
                gender=person['gender'],
                hair_color=person['hair_color'],
                height=person['height'],
                mass=person['mass'],
                homeworld=person['homeworld']
            ) for person in people_data if person['homeworld'] is not None
        ],ignore_conflicts=True)  # ignore_conflicts to skip duplicates based on unique constraints
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))