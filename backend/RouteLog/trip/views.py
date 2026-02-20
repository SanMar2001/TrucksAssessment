from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime
from .coordinates import get_coordinates, get_route

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

        coords = get_coordinates([current_location, pickup_location, dropoff_location])
        route = get_route(coords)

        return Response(route, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)