# modulo: src/exportadores/exportar_pdf.py
# descripcion: generacion de reportes pdf usando fpdf2
#-----------------------------------------------------------------------------

import os
from fpdf import FPDF
from src.modelos.contacto import Contacto
from src.logica import cargar_indice, leer_registro

ARCHIVO_EXPORT_PDF = 'exports/reporte_contactos.pdf'


class ReportePDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.titulo = 'Reporte de Agenda de Contactos'

    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, self.titulo, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', new_x="LMARGIN", new_y="NEXT", align='C')


def generar_reporte_pdf(ruta=ARCHIVO_EXPORT_PDF):
    """genera un archivo pdf con todos los contactos guardados en la agenda."""
    try:
        indice = cargar_indice()
        pdf = ReportePDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)
        
        if not indice:
            pdf.cell(0, 10, "No hay contactos registrados.", new_x="LMARGIN", new_y="NEXT")
        else:
            for id_k, num_reg in indice.items():
                contacto = leer_registro(num_reg)
                if contacto:
                    email_val = getattr(contacto, 'email', getattr(contacto, 'correo', ''))
                    # sanitizar texto para evitar errores de codificacion latin-1 en fpdf2
                    id_clean = str(contacto.id).strip().encode('latin-1', 'replace').decode('latin-1')
                    nom_clean = str(contacto.nombre).strip().encode('latin-1', 'replace').decode('latin-1')
                    tel_clean = str(contacto.telefono).strip().encode('latin-1', 'replace').decode('latin-1')
                    em_clean = str(email_val).strip().encode('latin-1', 'replace').decode('latin-1')

                    linea = f"ID: {id_clean} | Nombre: {nom_clean} | Tel: {tel_clean} | Email: {em_clean}"
                    pdf.cell(0, 8, linea, new_x="LMARGIN", new_y="NEXT")
        
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        pdf.output(ruta)
        return ruta, True
    except Exception as e:
        print(f"Error al generar reporte PDF: {e}")
        return None, False