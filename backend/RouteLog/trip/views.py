from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime
from .coordinates import get_coordinates, get_route
from .tripSimulation import process_trip
from .events import process_events

# Create your views here.
@api_view(['GET'])
def test(request):
    return JsonResponse({
        "status" : "Ok",
        "message" : "API Working",
        "datetime" : datetime.now()
    })

@api_view(['POST'])
def calculate(request):
    try:
        data = request.data

        current_location = data.get("currentLocation")
        pickup_location = data.get("pickupLocation")
        dropoff_location = data.get("dropoffLocation")
        cycle_used_hours = float(data.get("cycleUsedHours", 0))

        coords = get_coordinates([
            current_location,
            pickup_location,
            dropoff_location
        ])

        route = get_route(coords)
        
        route_a = route['routes'][0]['legs'][0]['distance']/ 1609.34
        route_b = route['routes'][0]['legs'][1]['distance']/ 1609.34
        print(f'{route_a:.2f}\n{route_b:.2f}\n{(route_a) + (route_b):.2f}')

        initial_state = {
            "current_time" : datetime.now(),
            "driving_hours": 0,
            "cycle_hours": cycle_used_hours,
            "trip_miles": 0
        }
        
        events = process_trip(route['routes'][0], initial_state)
        result = process_events(events)

        return Response({
            "route": route['routes'][0],
            "simulation": result
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)