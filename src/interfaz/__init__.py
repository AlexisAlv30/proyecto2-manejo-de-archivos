import tkinter as tk
from tkinter import ttk, messagebox
import os

# importaciones de los modulos de logica y exportadores
from src.logica import (
    leer_registro,
    escribir_registro,
    eliminar_registro,
    cargar_indice,
    verificar_integridad,
    actualizar_hash_sha256,
    obtener_metadatos_archivo,
    respaldo_completo,
)
from src.exportadores.exportar_json import exportar_a_json
from src.exportadores.exportar_pdf import generar_reporte_pdf
from src.modelos.contacto import Contacto


class InterfazAgenda:
    """clase principal de la interfaz grafica usando tkinter y ttk."""

    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos - Acceso Aleatorio (100 Bytes)")

        # contenedor principal de pestanas (notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # creacion de las 4 pestanas principales
        self.tab_contactos = ttk.Frame(self.notebook)
        self.tab_exportar = ttk.Frame(self.notebook)
        self.tab_herramientas = ttk.Frame(self.notebook)
        self.tab_ayuda = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_contactos, text="Contactos")
        self.notebook.add(self.tab_exportar, text="Exportar")
        self.notebook.add(self.tab_herramientas, text="Herramientas")
        self.notebook.add(self.tab_ayuda, text="Ayuda")

        # inicializar componentes de cada pestana
        self._construir_tab_contactos()
        self._construir_tab_exportar()
        self._construir_tab_herramientas()
        self._construir_tab_ayuda()

        # cargar registros existentes en la tabla
        self.actualizar_tabla_contactos()

    # -------------------------------------------------------------------------
    # PESTAÑA 1: GESTIÓN DE CONTACTOS (CRUD)
    # -------------------------------------------------------------------------
    def _construir_tab_contactos(self):
        # panel de formulario de entrada
        frame_form = ttk.LabelFrame(self.tab_contactos, text="Datos del Contacto", padding=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_id = ttk.Entry(frame_form)
        self.ent_id.grid(row=0, column=1, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nombre = ttk.Entry(frame_form)
        self.ent_nombre.grid(row=1, column=1, pady=5)

        ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_telefono = ttk.Entry(frame_form)
        self.ent_telefono.grid(row=2, column=1, pady=5)

        ttk.Label(frame_form, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_email = ttk.Entry(frame_form)
        self.ent_email.grid(row=3, column=1, pady=5)

        # botones de accion
        btn_guardar = ttk.Button(frame_form, text="Guardar / Actualizar", command=self.guardar_contacto)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        btn_eliminar = ttk.Button(frame_form, text="Eliminar Contacto", command=self.eliminar_contacto)
        btn_eliminar.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        btn_limpiar = ttk.Button(frame_form, text="Limpiar Campos", command=self.limpiar_formulario)
        btn_limpiar.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        # tabla de visualizacion (treeview)
        frame_tabla = ttk.Frame(self.tab_contactos, padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "nombre", "telefono", "email")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("email", text="Email")

        self.tabla.column("id", width=60)
        self.tabla.column("nombre", width=150)
        self.tabla.column("telefono", width=100)
        self.tabla.column("email", width=180)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_contacto)

    def guardar_contacto(self):
        """guarda o modifica un contacto utilizando registros fijos de 100 bytes."""
        id_val = self.ent_id.get().strip()
        nombre_val = self.ent_nombre.get().strip()
        tel_val = self.ent_telefono.get().strip()
        email_val = self.ent_email.get().strip()

        if not id_val or not nombre_val:
            messagebox.showwarning("Advertencia", "El ID y el Nombre son obligatorios.")
            return

        try:
            # se agrega el 5to argumento (ciudad) como cadena vacia para cumplir con Contacto.__init__
            contacto = Contacto(id_val, nombre_val, tel_val, email_val, "")
            num_reg, exito = escribir_registro(contacto)
            if exito:
                actualizar_hash_sha256()
                messagebox.showinfo("Éxito", f"Contacto guardado en el registro #{num_reg}.")
                self.limpiar_formulario()
                self.actualizar_tabla_contactos()
            else:
                messagebox.showerror("Error", "No se pudo guardar el contacto.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

    def eliminar_contacto(self):
        """elimina un contacto seleccionado y reorganiza el archivo."""
        id_val = self.ent_id.get().strip()
        if not id_val:
            messagebox.showwarning("Advertencia", "Seleccione o ingrese el ID del contacto a eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el contacto con ID {id_val}?"):
            if eliminar_registro(id_val):
                actualizar_hash_sha256()
                messagebox.showinfo("Éxito", "Contacto eliminado correctamente.")
                self.limpiar_formulario()
                self.actualizar_tabla_contactos()
            else:
                messagebox.showerror("Error", "No se encontró el contacto a eliminar.")

    def actualizar_tabla_contactos(self):
        """recarga la tabla de contactos leyendo desde el indice json y el archivo .dat."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        indice = cargar_indice()
        for id_k, num_reg in indice.items():
            contacto = leer_registro(num_reg)
            if contacto:
                email_val = getattr(contacto, 'email', getattr(contacto, 'correo', ''))
                self.tabla.insert("", "end", values=(contacto.id, contacto.nombre, contacto.telefono, email_val))

    def seleccionar_contacto(self, event):
        """llena los campos del formulario al hacer clic en un elemento de la tabla."""
        item_sel = self.tabla.selection()
        if item_sel:
            valores = self.tabla.item(item_sel[0], "values")
            self.limpiar_formulario()
            self.ent_id.insert(0, valores[0])
            self.ent_nombre.insert(0, valores[1])
            self.ent_telefono.insert(0, valores[2])
            self.ent_email.insert(0, valores[3])

    def limpiar_formulario(self):
        """limpia el contenido de las cajas de texto."""
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)

    # -------------------------------------------------------------------------
    # PESTAÑA 2: EXPORTACIÓN (JSON Y PDF)
    # -------------------------------------------------------------------------
    def _construir_tab_exportar(self):
        frame_exp = ttk.LabelFrame(self.tab_exportar, text="Exportación de Datos", padding=20)
        frame_exp.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame_exp, text="Exportar a JSON:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        ttk.Button(frame_exp, text="Generar archivo JSON", command=self.exportar_json).pack(anchor="w", pady=5)

        ttk.Separator(frame_exp, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(frame_exp, text="Exportar Reporte a PDF:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        ttk.Button(frame_exp, text="Generar Reporte PDF (fpdf2)", command=self.exportar_pdf).pack(anchor="w", pady=5)

    def exportar_json(self):
        ruta, exito = exportar_a_json()
        if exito:
            messagebox.showinfo("Éxito", f"Datos exportados a JSON en:\n{ruta}")
        else:
            messagebox.showerror("Error", "No se pudo exportar a JSON.")

    def exportar_pdf(self):
        ruta, exito = generar_reporte_pdf()
        if exito:
            messagebox.showinfo("Éxito", f"Reporte PDF generado en:\n{ruta}")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte PDF.")

    # -------------------------------------------------------------------------
    # PESTAÑA 3: HERRAMIENTAS (INTEGRIDAD SHA-256, ZIP Y METADATOS)
    # -------------------------------------------------------------------------
    def _construir_tab_herramientas(self):
        frame_herramientas = ttk.Frame(self.tab_herramientas, padding=15)
        frame_herramientas.pack(fill="both", expand=True)

        # verificacion sha-256
        frame_sha = ttk.LabelFrame(frame_herramientas, text="Integridad de Datos (SHA-256)", padding=10)
        frame_sha.pack(fill="x", pady=5)

        ttk.Button(frame_sha, text="Verificar Integridad del Archivo .dat", command=self.verificar_sha).pack(side="left", padx=5)

        # respaldo zip
        frame_zip = ttk.LabelFrame(frame_herramientas, text="Respaldos Comprimidos", padding=10)
        frame_zip.pack(fill="x", pady=5)

        ttk.Button(frame_zip, text="Generar Respaldo ZIP (.dat + .json)", command=self.crear_respaldo).pack(side="left", padx=5)

        # metadatos del archivo
        frame_meta = ttk.LabelFrame(frame_herramientas, text="Metadatos del Archivo (os.stat)", padding=10)
        frame_meta.pack(fill="both", expand=True, pady=5)

        ttk.Button(frame_meta, text="Obtener Metadatos de contactos.dat", command=self.mostrar_metadatos).pack(anchor="w", pady=5)
        self.lbl_metadatos = ttk.Label(frame_meta, text="Haga clic para obtener metadatos...", font=("Consolas", 9))
        self.lbl_metadatos.pack(anchor="w", pady=5)

    def verificar_sha(self):
        es_intacto, msj = verificar_integridad()
        if es_intacto:
            messagebox.showinfo("Integridad Correcta", msj)
        else:
            messagebox.showwarning("Alerta de Integridad", msj)

    def crear_respaldo(self):
        ruta_zip, orig, comp = respaldo_completo()
        if ruta_zip:
            messagebox.showinfo("Respaldo Creado", f"Respaldo generado en:\n{ruta_zip}\n\nTamaño original: {orig} bytes\nTamaño ZIP: {comp} bytes")
        else:
            messagebox.showerror("Error", "No se pudo crear el respaldo ZIP.")

    def mostrar_metadatos(self):
        meta = obtener_metadatos_archivo()
        if meta:
            texto = (
                f"Ruta: {meta['ruta']}\n"
                f"Tamaño: {meta['tamano_bytes']} bytes\n"
                f"Última modificación: {meta['fecha_modificacion']}\n"
                f"Último acceso: {meta['fecha_acceso']}\n"
                f"Permisos: {meta['permisos']}"
            )
            self.lbl_metadatos.config(text=texto)
        else:
            self.lbl_metadatos.config(text="No se encontró el archivo de contactos.")

    # -------------------------------------------------------------------------
    # PESTAÑA 4: AYUDA E INFORMACIÓN
    # -------------------------------------------------------------------------
    def _construir_tab_ayuda(self):
        frame_ayuda = ttk.Frame(self.tab_ayuda, padding=20)
        frame_ayuda.pack(fill="both", expand=True)

        info_texto = (
            "Laboratorio No. 2: Agenda de Contactos con Acceso Aleatorio\n\n"
            "• Registros de Tamaño Fijo: Cada registro ocupa exactamente 100 bytes.\n"
            "• Acceso Aleatorio: Uso directo de seek() y tell() para lectura y modificacion in situ.\n"
            "• Indice Primario JSON: Asocia el ID del contacto con su numero de registro.\n"
            "• Integridad SHA-256: Hash de verificacion para detectar cambios externos.\n"
            "• Exportacion y Respaldos: Generacion de reportes PDF, exportacion JSON y ZIP comprimido.\n\n"
            "Desarrollado para la materia de Estructura de Datos."
        )

        lbl_info = ttk.Label(frame_ayuda, text=info_texto, font=("Arial", 10), justify="left")
        lbl_info.pack(anchor="nw")