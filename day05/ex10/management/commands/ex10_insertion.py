from django.core.management.base import BaseCommand
from data.service import DataService
from ex10.models import Planet, Person, Movies

class Command(BaseCommand):
    help = 'Inserts data into the Planet and Person models from the Star Wars API'

    def handle(self, *args, **kwargs):
        try:
                service = DataService()
                data = service.get_ex10_initials()
                people_data = []
                Planet_data = []
                movies_data = []
                def find_planet(num):
                    #  print(f"Looking for planet with pk: {num}")
                    if num is None:
                            return None
                    for item in Planet_data:
                        if item['pk'] == num:
                            print(f"Found planet: {item['name']} for pk: {num}")
                            return item['name']
                    return None
                def find_characters(nums):
                    print(f"Looking for characters with pks: {nums}")
                    characters = []
                    if nums is None:
                            return None
                    for num in nums:
                        for item in people_data:
                            if item['pk'] == num:
                                print(f"Found character: {item['name']} for pk: {num}")
                                characters.append(item['name'])
                    return characters
                    
                for item in data:
                    if item['model'] == 'ex10.planets':
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


                for item in data:
                    if item['model'] == 'ex10.people':
                        people_data.append({
                            'name': item['fields']['name'],
                            'birth_year': item['fields']['birth_year'],
                            'eye_color': item['fields']['eye_color'],
                            'gender': item['fields']['gender'],
                            'hair_color': item['fields']['hair_color'],
                            'height': item['fields']['height'],
                            'mass': item['fields']['mass'],
                            'homeworld': find_planet(item['fields']['homeworld']),
                            'pk': item['pk']  # keep pk for lookup only
                        })

                for item in data:
                    if item['model'] == 'ex10.movies':
                        movies_data.append({
                            'episode_nb': item['pk'],
                            'title': item['fields']['title'],
                            'opening_crawl': item['fields']['opening_crawl'],
                            'director': item['fields']['director'],
                            'producer': item['fields']['producer'],
                            'release_date': item['fields']['release_date'],
                            'characters': find_characters(item['fields']['characters']),
                            'pk': item['pk']  # keep pk for lookup only
                        })

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
                    ],ignore_conflicts=True) 
                Person.objects.bulk_create([
                    Person(
                        name=person['name'],
                        birth_year=person['birth_year'],
                        eye_color=person['eye_color'],
                        gender=person['gender'],
                        hair_color=person['hair_color'],
                        height=person['height'],
                        mass=person['mass'],
                        homeworld=Planet.objects.get(name=find_planet(person['homeworld'])) if find_planet(person['homeworld']) else None
                    ) for person in people_data if person['homeworld'] is not None
                    ],ignore_conflicts=True)
                movies_instances = Movies.objects.bulk_create([
                    Movies(
                        episode_nb=movie['episode_nb'],
                        title=movie['title'],
                        opening_crawl=movie['opening_crawl'],
                        director=movie['director'],
                        producer=movie['producer'],
                        release_date=movie['release_date']
                    ) for movie in movies_data
                ], ignore_conflicts=True)

                # Set many-to-many characters after creation
                for movie_obj, movie_data in zip(movies_instances, movies_data):
                    character_names = movie_data['characters']
                    if character_names:
                        persons = Person.objects.filter(name__in=character_names)
                        movie_obj.characters.set(persons)
                                      
                self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.stderr.write(self.style.ERROR(f"Error inserting data: {e}"))