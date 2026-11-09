import os
import json

# Rutas por defecto - se pueden sobreescribir
ARCHIVO_INDICE = 'data/indice.json'


def cargar_indice():
    """Carga y retorna el diccionario de índice desde el archivo JSON.
    
    Estructura: {id: num_registro}
    
    Retorna:
        dict: Diccionario con el índice de contactos
    """
    try:
        if os.path.exists(ARCHIVO_INDICE):
            with open(ARCHIVO_INDICE, 'r', encoding='utf-8') as f:
                indice = json.load(f)
            return indice
        return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def guardar_indice(indice):
    """Guarda el diccionario de índice en el archivo JSON.
    
    Argumentos:
        indice (dict): Diccionario {id: num_registro} a guardar.
    """
    try:
        with open(ARCHIVO_INDICE, 'w', encoding='utf-8') as f:
            json.dump(indice, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f'Error guardando índice: {e}')


def obtener_siguiente_num_registro():
    """Obtiene el siguiente número de registro disponible.
    
    Busca el máximo num_registro actual en el índice y suma 1.
    Si el índice está vacío, retorna 0.
    
    Retorna:
        int: Próximo número de registro disponible
    """
    indice = cargar_indice()
    if not indice:
        return 0
    return max(indice.values()) + 1


def verificar_id_existe(id_):
    """Verifica si un ID ya existe en el índice.
    
    Argumentos:
        id_: Identificador a verificar
    
    Retorna:
        bool: True si el ID existe, False si no
    """
    indice = cargar_indice()
    return str(id_) in indice


def obtener_num_registro(id_):
    """Obtiene el número de registro asociado a un ID.
    
    Argumentos:
        id_: Identificador del contacto
    
    Retorna:
        int or None: Número de registro si existe, None si no
    """
    indice = cargar_indice()
    return indice.get(str(id_))