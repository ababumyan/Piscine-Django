import csv
import os
import json
class DataService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.planets_path = os.path.join(base_dir, 'planets.csv')
        self.people_path = os.path.join(base_dir, 'people.csv')

    def read_csv(self, path, fieldnames):
        with open(path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t', fieldnames=fieldnames)
            data = [row for row in reader]
        return data
    
    def get_planets_data(self):
        fieldnames = ['name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain']
        return self.read_csv(self.planets_path, fieldnames)
    
    def get_people_data(self):
        fieldnames = ['name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld']
        return self.read_csv(self.people_path, fieldnames)
    
    def get_initial_data(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex09_initial_data.json'), 'r') as json_file:
            data = json.load(json_file)
        return data
    
    def get_ex10_initials(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex10_initial_data.json'), 'r') as json_file:
            data = json.load(json_file)
        return data