# modulo: src/exportadores/exportar_json.py
# descripcion: exportacion de contactos a formato json
#-----------------------------------------------------------------------------

import json
import os
from src.modelos.contacto import Contacto
from src.logica import cargar_indice, leer_registro

# rutas por defecto
RUTA_DEFAULT = 'exports/contactos_exportados.json'


def exportar_lista_contactos(contactos, ruta_archivo=None):
    """exporta una lista de objetos contacto a un archivo json.
    
    convierte cada objeto contacto a un diccionario con sus campos desformateados,
    luego guarda la lista en un archivo json con estructura legible.
    """
    if ruta_archivo is None:
        ruta_archivo = RUTA_DEFAULT
    
    try:
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        
        datos = []
        for c in contactos:
            if c is not None:
                # soporta los atributos de contacto adaptados a la aplicacion
                email_val = getattr(c, 'email', getattr(c, 'correo', ''))
                datos.append({
                    'id': c.id.strip(),
                    'nombre': c.nombre.strip(),
                    'telefono': c.telefono.strip(),
                    'email': email_val.strip()
                })
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        return ruta_archivo, True
    except Exception as e:
        print(f'error exportando a json: {e}')
        return None, False


def exportar_a_json(ruta_archivo=None):
    """funcion requerida por main.py e interfaz grafica.
    
    lee todos los contactos desde el archivo binario usando el indice json
    y los exporta al archivo destino.
    """
    try:
        indice = cargar_indice()
        contactos = []
        for id_k, num_reg in indice.items():
            c = leer_registro(num_reg)
            if c:
                contactos.append(c)
        return exportar_lista_contactos(contactos, ruta_archivo)
    except Exception as e:
        print(f'error al exportar a json: {e}')
        return None, False


def exportar_contacto_individual(contacto, ruta_archivo=None):
    """exporta un solo contacto a formato json."""
    if ruta_archivo is None:
        ruta_archivo = os.path.join('exports', f'contacto_{contacto.id.strip()}.json')
    
    try:
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        email_val = getattr(contacto, 'email', getattr(contacto, 'correo', ''))
        
        datos = {
            'id': contacto.id.strip(),
            'nombre': contacto.nombre.strip(),
            'telefono': contacto.telefono.strip(),
            'email': email_val.strip()
        }
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        return ruta_archivo
    except Exception as e:
        print(f'error exportando contacto individual: {e}')
        return None