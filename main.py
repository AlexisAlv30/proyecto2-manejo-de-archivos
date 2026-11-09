# punto de entrada principal de la aplicacion Agenda de Contactos con acceso aleatorio
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from src.modelos.contacto import Contacto
from src.logica import (
    inicializar_archivo,
    leer_registro,
    escribir_registro,
    cargar_indice,
    verificar_integridad,
    actualizar_hash_sha256,
    obtener_metadatos_archivo,
    respaldo_completo,
)
from src.logica.sha256 import calcular_hash, guardar_hash
from src.exportadores.exportar_json import exportar_a_json
from src.exportadores.exportar_pdf import generar_reporte_pdf
from src.interfaz import InterfazAgenda

def main():
    """Punto de entrada de la aplicacion de agenda de contactos."""
    # Inicializar los archivos de datos (crearlos si no existen)
    inicializar_archivo()

    # Crear la ventana principal de la aplicacion
    root_ttk = tk.Tk()
    root_ttk.title("Agenda de Contactos - Laboratorio No. 2")
    root_ttk.geometry("900x600")
    root_ttk.minsize(800, 500)

    # Estilo personalizado para ttk
    style = ttk.Style()
    style.theme_use('clam')

    # Instanciar la clase de la interfaz grafica
    aplicacion = InterfazAgenda(root_ttk)

    # Iniciar el bucle principal de eventos
    root_ttk.mainloop()

if __name__ == "__main__":
    main()