class Contacto:
    """Clase que representa un contacto de la agenda con empaquetado exacto de 100 bytes en UTF-8."""

    TAMANIO_REGISTRO = 100
    TAM_ID = 10
    TAM_NOMBRE = 30
    TAM_TELEFONO = 15
    TAM_CORREO = 45

    def __init__(self, id_, nombre, telefono, correo, ciudad=""):
        """Inicializa un nuevo contacto limpiando espacios laterales."""
        self.id = str(id_).strip()
        self.nombre = str(nombre).strip()
        self.telefono = str(telefono).strip()
        self.correo = str(correo).strip()
        self.ciudad = str(ciudad).strip()

    def a_registro(self):
        """Convierte el objeto Contacto a un registro binario de exactamente 100 bytes en UTF-8."""
        id_bytes = self.id.encode('utf-8')[:self.TAM_ID].ljust(self.TAM_ID, b' ')
        nombre_bytes = self.nombre.encode('utf-8')[:self.TAM_NOMBRE].ljust(self.TAM_NOMBRE, b' ')
        tel_bytes = self.telefono.encode('utf-8')[:self.TAM_TELEFONO].ljust(self.TAM_TELEFONO, b' ')
        correo_bytes = self.correo.encode('utf-8')[:self.TAM_CORREO].ljust(self.TAM_CORREO, b' ')

        registro_bytes = id_bytes + nombre_bytes + tel_bytes + correo_bytes
        
        if len(registro_bytes) < self.TAMANIO_REGISTRO:
            registro_bytes = registro_bytes.ljust(self.TAMANIO_REGISTRO, b' ')
            
        return registro_bytes[:self.TAMANIO_REGISTRO]

    @staticmethod
    def de_registro(registro_bytes):
        """Crea un objeto Contacto a partir de un bloque binario de 100 bytes alineados."""
        if not registro_bytes or len(registro_bytes) != Contacto.TAMANIO_REGISTRO:
            raise ValueError(f'Registro corrupto: se esperaban {Contacto.TAMANIO_REGISTRO} bytes, '
                             f'pero se recibieron {len(registro_bytes) if registro_bytes else 0} bytes')

        id_ = registro_bytes[0:10].decode('utf-8', errors='ignore').strip()
        nombre = registro_bytes[10:40].decode('utf-8', errors='ignore').strip()
        telefono = registro_bytes[40:55].decode('utf-8', errors='ignore').strip()
        correo = registro_bytes[55:100].decode('utf-8', errors='ignore').strip()

        return Contacto(id_, nombre, telefono, correo)

    def a_dict(self):
        """Retorna la representación del contacto en formato diccionario para JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.correo
        }

    def __str__(self):
        return (f'ID: {self.id} | Nombre: {self.nombre} | '
                f'Tel: {self.telefono} | Mail: {self.correo}')