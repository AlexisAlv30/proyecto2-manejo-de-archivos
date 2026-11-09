import os
from src.modelos.contacto import Contacto
from src.logica.indice import cargar_indice, guardar_indice

ARCHIVO_CONTACTOS = 'data/contactos.dat'
ARCHIVO_INDICE = 'data/indice.json'


def inicializar_archivo():
    """Inicializa la estructura creando el directorio data y los archivos si no existen."""
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists(ARCHIVO_CONTACTOS):
        with open(ARCHIVO_CONTACTOS, 'wb') as f:
            pass
            
    if not os.path.exists(ARCHIVO_INDICE):
        guardar_indice({})


def definir_posicion(num_registro):
    """Calcula la posición en bytes para un número de registro usando seek()."""
    return num_registro * Contacto.TAMANIO_REGISTRO


def leer_registro(num_registro):
    """Lee un registro específico del archivo usando seek() y tell()."""
    try:
        inicializar_archivo()
        posicion = definir_posicion(num_registro)
        
        with open(ARCHIVO_CONTACTOS, 'rb') as f:
            f.seek(posicion)
            datos = f.read(Contacto.TAMANIO_REGISTRO)
            posicion_actual = f.tell()  # Método tell(): reporta ubicación en bytes
        
        if not datos or len(datos) < Contacto.TAMANIO_REGISTRO or datos.strip() == b'':
            return None
        
        return Contacto.de_registro(datos)
    except Exception as e:
        print(f'Error al leer registro #{num_registro}: {e}')
        return None


def escribir_registro(contacto, num_registro=None):
    """Escribe o actualiza un registro en el archivo binario usando seek() para modificación in situ."""
    try:
        inicializar_archivo()
        indice = cargar_indice()
        id_str = contacto.id.strip()

        if id_str in indice:
            num_registro = indice[id_str]
        elif num_registro is None:
            num_registro = len(indice)
            indice[id_str] = num_registro
            guardar_indice(indice)

        posicion = definir_posicion(num_registro)
        registro_bytes = contacto.a_registro()

        modo = 'r+b' if os.path.exists(ARCHIVO_CONTACTOS) and os.path.getsize(ARCHIVO_CONTACTOS) > 0 else 'wb'
        with open(ARCHIVO_CONTACTOS, modo) as f:
            f.seek(posicion)
            f.write(registro_bytes)

        return num_registro, True

    except Exception as e:
        print(f'Error al escribir registro: {e}')
        return num_registro, False


def eliminar_registro(id_):
    """Elimina un registro del archivo binario y reindexa los números de registro."""
    try:
        inicializar_archivo()
        indice = cargar_indice()
        id_str = str(id_).strip()

        if id_str not in indice:
            return False

        num_registro = indice[id_str]

        with open(ARCHIVO_CONTACTOS, 'rb') as f:
            f.seek(0, 2)
            f.seek(0)
            todos_datos = f.read()

        inicio = num_registro * Contacto.TAMANIO_REGISTRO
        fin = inicio + Contacto.TAMANIO_REGISTRO
        datos_nuevos = todos_datos[:inicio] + todos_datos[fin:]

        with open(ARCHIVO_CONTACTOS, 'wb') as f:
            f.write(datos_nuevos)

        del indice[id_str]
        indice_actualizado = {}
        for key, value in indice.items():
            if value > num_registro:
                indice_actualizado[key] = value - 1
            else:
                indice_actualizado[key] = value

        guardar_indice(indice_actualizado)
        return True

    except Exception as e:
        print(f'Error al eliminar registro: {e}')
        return False