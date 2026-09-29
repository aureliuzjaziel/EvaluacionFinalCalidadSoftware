# app_usuarios/services/usuario_service.py
import requests
from app_usuarios.models import Usuario

API_URL = "https://randomuser.me/api/"
API_PARAMS = {"page": 3, "results": 10, "seed": "Evaluacion_final_Xavier_Lagos"}

def get_usuarios_api():
    try:
        respuesta = requests.get(API_URL, params=API_PARAMS, timeout=10)
        respuesta.raise_for_status()
        if respuesta.status_code == 200:
            return respuesta.json().get('results', [])
    except (requests.RequestException, ValueError):
        return None
    return None

def load_usuarios():
    
    if Usuario.objects.exists():
        return f"Usuarios ya cargados. Total: {Usuario.objects.count()}"

    usuarios_api = get_usuarios_api()
    if usuarios_api is None:
        return "No se pudieron cargar los usuarios desde la API."

    for u in usuarios_api:
        Usuario.objects.create(
            uuid=u['login']['uuid'],
            nombre_completo=f"{u['name']['title']} {u['name']['first']} {u['name']['last']}",
            email=u['email'],
            genero=u['gender'].upper(),
            edad=u['dob']['age'],
            ciudad=u['location']['city'],
            imagen_large=u['picture']['large'],
            imagen_medium=u['picture']['medium'],
            imagen_thumbnail=u['picture']['thumbnail'],
            fecha_registro=u['registered']['date']
        )
    return f"Éxito: Se guardaron {Usuario.objects.count()} usuarios."
