import requests

def get_coordinates(cities):
    if cities:
        coords = []
        for city in cities:
            url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
            headers = {"User-Agent": "route-planner-app"}
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                if not data:
                    raise ValueError("City not found")
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                coords.append((lat, lon))
            except Exception as e:
                print(f"Error getting coordinates for {city}: {e}")
                return None, None
        return coords
    else:
        raise ValueError("Error loading cities")


def get_route(coords_list):
    if not coords_list or len(coords_list) < 2:
        print("Se necesitan al menos 2 coordenadas para calcular la ruta")
        return None

    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords_list])
    url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson&annotations=duration,distance"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error calculating route: {e}")
        return None