import requests

# URL del endpoint Flask
url = 'https://localhost:5800/signup/v1'

# Lista de usuarios (nombre completo)
usuarios = [
    "Enrique Acosta",
    "Rolando Salazar",
    "Rodrigo Gonzalez",
    "Victor Villalobos"
]

# Contraseña común
password = "clave123"

# Desactivar advertencias por certificado autofirmado
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enviar cada usuario
for usuario in usuarios:
    data = {
        "username": usuario,
        "password": password
    }
    try:
        response = requests.post(url, data=data, verify=False)
        print(f"Registrando '{usuario}' → Respuesta: {response.text}")
    except Exception as e:
        print(f"Error con usuario '{usuario}': {e}")
