# modulo: src/logica/metadatos.py
# descripcion: modulo independiente para obtener metadatos de archivo usando os.stat()
#-----------------------------------------------------------------------------


import os
import time

# rutas por defecto - se pueden sobreescribir
ARCHIVO_CONTACTOS = 'data/contactos.dat'


def obtener_estadisticas(ruta_archivo=None):
    """obtiene metadatos del archivo de contactos usando os.stat().
    
    usa os.stat() para obtener informacion del archivo incluyendo:
    - tamano en bytes
    - fecha y hora de ultima modificacion
    - fecha y hora de ultimo acceso
    - permisos del archivo
    
    argumentos:
        ruta_archivo (str, optional): ruta del archivo a inspeccionar.
            si es None, usa la ruta por defecto.
            
    retorna:
        dict: diccionario con los metadatos del archivo, o None si no existe
            - tamano_bytes (int): tamano en bytes del archivo
            - ultima_modificacion (float): marca de tiempo de ultima modificacion
            - ultimo_acceso (float): marca de tiempo de ultimo acceso
            - permisos (str): representacion octal de los permisos
            - ruta (str): ruta del archivo
    """
    if ruta_archivo is None:
        ruta_archivo = ARCHIVO_CONTACTOS
        
    try:
        if os.path.exists(ruta_archivo):
            estadisticas = os.stat(ruta_archivo)
            return {
                'tamano_bytes': estadisticas.st_size,
                'ultima_modificacion': estadisticas.st_mtime,
                'ultimo_acceso': estadisticas.st_atime,
                'permisos': oct(estadisticas.st_mode),
                'ruta': ruta_archivo
            }
        return None
    except Exception as e:
        print(f'error obteniendo metadatos: {e}')
        return None


def formatear_fecha(marca_tiempo):
    """formatea una marca de tiempo de os.stat() en string legible.
    
    argumentos:
        marca_tiempo (float): marca de tiempo de epoch
    
    retorna:
        str: fecha y hora formateada en formato 'YYYY-MM-DD HH:MM:SS'
    """
    if marca_tiempo is None:
        return 'n/a'
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(marca_tiempo))


def obtener_metadatos_archivo(ruta_archivo=None):
    """funcion alias para resolver la importacion requerida por main.py y el paquete logica.
    
    retorna un diccionario estructurado con los metadatos listos para la interfaz grafica.
    """
    stats = obtener_estadisticas(ruta_archivo)
    if not stats:
        return None
        
    return {
        'tamano_bytes': stats['tamano_bytes'],
        'fecha_modificacion': formatear_fecha(stats['ultima_modificacion']),
        'fecha_acceso': formatear_fecha(stats['ultimo_acceso']),
        'permisos': stats['permisos'],
        'ruta': stats['ruta']
    }