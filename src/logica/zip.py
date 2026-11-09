# modulo: src/logica/zip.py
# descripcion: Generación de respaldos comprimidos ZIP (.dat + .json)
#-----------------------------------------------------------------------------

import os
import zipfile
from datetime import datetime

ARCHIVO_CONTACTOS = 'data/contactos.dat'
ARCHIVO_INDICE = 'data/indice.json'
DIR_EXPORTS = 'exports'


def crear_respaldo_zip():
    """Crea un archivo ZIP con la fecha actual que respalda contactos.dat e indice.json."""
    try:
        os.makedirs(DIR_EXPORTS, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_zip = f'respaldo_{timestamp}.zip'
        ruta_zip = os.path.join(DIR_EXPORTS, nombre_zip)

        archivos_a_respaldar = [ARCHIVO_CONTACTOS, ARCHIVO_INDICE]
        
        tamano_original = 0
        with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for archivo in archivos_a_respaldar:
                if os.path.exists(archivo):
                    tamano_original += os.path.getsize(archivo)
                    zipf.write(archivo, os.path.basename(archivo))

        tamano_comprimido = os.path.getsize(ruta_zip)
        ahorro = ((tamano_original - tamano_comprimido) / tamano_original * 100) if tamano_original > 0 else 0

        print(f"Respaldo creado: {ruta_zip}")
        print(f"Tamaño original: {tamano_original} bytes")
        print(f"Tamaño comprimido: {tamano_comprimido} bytes")
        print(f"Ahorro: {ahorro:.1f}%")

        return ruta_zip, tamano_original, tamano_comprimido, True

    except Exception as e:
        print(f"Error al crear respaldo ZIP: {e}")
        return None, 0, 0, False

def respaldo_completo():
    """Alias de compatibilidad para llamadas antiguas."""
    return crear_respaldo_zip()