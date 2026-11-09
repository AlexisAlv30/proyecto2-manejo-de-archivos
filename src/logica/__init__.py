# modulo: src/logica/__init__.py
# descripcion: paquete principal de logica - reexporta funcionalidades de modulos subordinados
#-----------------------------------------------------------------------------

# funciones de lectura/escritura con seek() y tell()
from .lectura_escritura import (
    definir_posicion,
    leer_registro,
    escribir_registro,
    eliminar_registro,
    inicializar_archivo,
)

# funciones de gestion de indice json
from .indice import (
    cargar_indice,
    guardar_indice,
    obtener_siguiente_num_registro,
    verificar_id_existe,
    obtener_num_registro,
)

# funciones de hash sha-256
from .sha256 import (
    calcular_hash,
    guardar_hash,
    verificar_integridad,
    actualizar_hash_sha256,
)

# funciones de respaldo zip
from .zip import crear_respaldo_zip, respaldo_completo

# funciones de metadatos con os.stat()
from .metadatos import obtener_metadatos_archivo

# importacion del modelo de contactos
from src.modelos.contacto import Contacto

# tamano fijo de registro
TAMANIO_REGISTRO = 100

# variables de ruta por defecto
ARCHIVO_CONTACTOS = 'data/contactos.dat'
ARCHIVO_INDICE = 'data/indice.json'
ARCHIVO_SHA256 = 'data/contactos.sha256'