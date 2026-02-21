from django.db import models

# Create your models here.
class Leg():
    def __init__(self, distance, duration, coordinates, index):
        self.distance = distance
        self.duration = duration
        self.coordinates = coordinates
        self.index = index