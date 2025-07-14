import requests

api_key = '5b3ce3597851110001cf6248d699eb49cea14e3daecfcc93936c6609'

def geocode_location(place_name):
    geocode_url = 'https://api.openrouteservice.org/geocode/search'
    params = {
        'api_key': api_key,
        'text': place_name,
        'size': 1
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()
    
    try:
        coords = data['features'][0]['geometry']['coordinates']  # [lon, lat]
        display_name = data['features'][0]['properties']['label']
        return coords, display_name
    except (KeyError, IndexError):
        print(f"No se pudo geocodificar: {place_name}")
        return None, None

def get_travel_info(origin_coords, destination_coords, origin_name, destination_name, mode):
    modes_dict = {
        "auto": "driving-car",
        "bicicleta": "cycling-regular",
        "a pie": "foot-walking"
    }

    if mode not in modes_dict:
        print("Modo de transporte no válido. Usando 'auto' por defecto.")
        mode = "auto"

    directions_url = f'https://api.openrouteservice.org/v2/directions/{modes_dict[mode]}'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        'coordinates': [origin_coords, destination_coords]
    }

    response = requests.post(directions_url, json=body, headers=headers)
    data = response.json()

    try:
        summary = data['routes'][0]['summary']
        duration = int(summary['duration'])  # segundos
        distance_m = summary['distance']     # metros
        distance_km = distance_m / 1000
        distance_mi = distance_km * 0.621371

        # Calcular duración
        hours = duration // 3600
        minutes = (duration % 3600) // 60

        # Calcular combustible si es en auto
        consumo_km_por_litro = 10
        litros = distance_km / consumo_km_por_litro if mode == "auto" else 0

        # Mostrar resumen
        print("\n🗺️  Resumen del viaje:")
        print(f"Desde: {origin_name}")
        print(f"Hasta: {destination_name}")
        print(f"Transporte: {mode}")
        print(f"Distancia: {distance_km:.2f} km / {distance_mi:.2f} millas")
        print(f"Duración estimada: {hours}h {minutes}m")
        if mode == "auto":
            print(f"Combustible estimado: {litros:.2f} litros")
        
        # Narrativa
        print(f"\n📍 Viajarás de {origin_name} a {destination_name} en {mode}, recorriendo aproximadamente {distance_km:.1f} km.")
        print(f"El viaje tomará cerca de {hours} horas y {minutes} minutos.")
        if mode == "auto":
            print(f"Necesitarás alrededor de {litros:.1f} litros de combustible.\n")
        print("¡Buen viaje! 🧳\n")

    except (KeyError, IndexError):
        print("No se pudo obtener la información del viaje.")

# 🔁 Loop principal
while True:
    print("\n--- Planificador de Viaje 🇨🇱🇦🇷 ---")
    origen_input = input("Ingrese la ciudad de ORIGEN (o 's' para salir): ")
    if origen_input.lower() == 's':
        break

    destino_input = input("Ingrese la ciudad de DESTINO (o 's' para salir): ")
    if destino_input.lower() == 's':
        break

    print("Tipos de transporte: auto, bicicleta, a pie")
    modo = input("Seleccione el tipo de transporte: ").lower()
    if modo == 's':
        break

    # Geocodificación
    origen_coords, origen_nombre = geocode_location(origen_input)
    destino_coords, destino_nombre = geocode_location(destino_input)

    if origen_coords and destino_coords:
        get_travel_info(origen_coords, destino_coords, origen_nombre, destino_nombre, modo)
