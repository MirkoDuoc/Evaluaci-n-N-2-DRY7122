import requests

# API keys (si son necesarias)
ORS_API_KEY = '5b3ce3597851110001cf624825b1b8de0fef41c8978898e2aa1de58f'

# Función para obtener coordenadas de una ciudad usando Nominatim
def get_coordinates(city):
    url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'
    response = requests.get(url)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        return None, None

# Función para obtener la ruta entre dos puntos usando OpenRouteService
def get_route(start, end):
    url = f'https://api.openrouteservice.org/v2/directions/driving-car'
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        'coordinates': [start, end],
        'format': 'json'
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if data and 'routes' in data:
        return data['routes'][0]
    else:
        return None

# Función para calcular el consumo de combustible estimado
def calculate_fuel(distance_km, fuel_efficiency_l_per_100km=8.5):
    return (distance_km * fuel_efficiency_l_per_100km) / 100

# Solicitar entrada del usuario
def main():
    while True:
        origen = input("Ciudad de Origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            break
        destino = input("Ciudad de Destino: ")

        start_lat, start_lon = get_coordinates(origen)
        end_lat, end_lon = get_coordinates(destino)

        if start_lat and end_lat:
            route = get_route([start_lon, start_lat], [end_lon, end_lat])
            if route:
                distance_km = route['summary']['distance'] / 1000
                duration_sec = route['summary']['duration']
                fuel_needed_l = calculate_fuel(distance_km)

                hours, remainder = divmod(duration_sec, 3600)
                minutes, seconds = divmod(remainder, 60)

                print(f"\nDistancia: {distance_km:.2f} km")
                print(f"Duración: {int(hours)}h {int(minutes)}m {int(seconds)}s")
                print(f"Combustible requerido: {fuel_needed_l:.2f} litros")
                print(f"Narrativa del viaje: {route['segments'][0]['steps']}")
            else:
                print("No se pudo calcular la ruta.")
        else:
            print("No se pudo obtener coordenadas para las ciudades especificadas.")

if __name__ == '__main__':
    main()
