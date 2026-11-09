# modulo: src/logica/sha256.py
# descripcion: modulo independiente para verificacion y calculo de hash sha-256
#-----------------------------------------------------------------------------

import hashlib
import os

ARCHIVO_CONTACTOS = 'data/contactos.dat'
ARCHIVO_SHA256 = 'data/contactos.sha256'


def calcular_hash(archivo_ruta=None):
    """Calcula el hash SHA-256 de un archivo binario en bloques de 8KB."""
    if archivo_ruta is None:
        archivo_ruta = ARCHIVO_CONTACTOS

    try:
        if not os.path.exists(archivo_ruta):
            os.makedirs(os.path.dirname(archivo_ruta), exist_ok=True)
            with open(archivo_ruta, 'wb') as f:
                pass
            return ''

        sha256_hash = hashlib.sha256()
        with open(archivo_ruta, 'rb') as f:
            for bloque in iter(lambda: f.read(8192), b''):
                sha256_hash.update(bloque)

        return sha256_hash.hexdigest()
    except Exception as e:
        print(f'Error calculando hash SHA-256: {e}')
        return None


def guardar_hash():
    """Calcula y guarda el hash SHA-256 en el archivo de metadatos."""
    hash_calculado = calcular_hash()
    try:
        if os.path.dirname(ARCHIVO_SHA256):
            os.makedirs(os.path.dirname(ARCHIVO_SHA256), exist_ok=True)
        with open(ARCHIVO_SHA256, 'w', encoding='utf-8') as f:
            f.write(hash_calculado if hash_calculado else '')
        return hash_calculado
    except IOError as e:
        print(f'Error guardando hash: {e}')
        return None


def actualizar_hash_sha256():
    """Función de enlace para recalcular y guardar el hash SHA-256."""
    return guardar_hash()


def verificar_integridad():
    """Verifica la integridad del archivo retornando (es_correcto, mensaje) para la UI."""
    hash_actual = calcular_hash()

    if not os.path.exists(ARCHIVO_SHA256):
        guardar_hash()
        return True, "Hash inicial creado y verificado correctamente."

    try:
        with open(ARCHIVO_SHA256, 'r', encoding='utf-8') as f:
            hash_guardado = f.read().strip()

        if hash_actual is None:
            return False, "Error al leer el archivo binario."

        if hash_actual == hash_guardado:
            return True, f"Integridad correcta: El archivo binario no ha sido modificado.\nHASH: {hash_actual[:16]}..."
        else:
            return False, "¡Advertencia! El archivo binario ha sido alterado externamente."

    except Exception as e:
        print(f'Error verificando integridad: {e}')
        return False, f"Error al verificar la integridad: {e}"