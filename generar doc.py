import os
from reportlab.platypus import Paragraph, TableStyle
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import sqlite3 as dbapi

bd = dbapi.connect("e.dat")
cursor = bd.cursor()

cursor.execute("select * from clientes")
tablaBaseDatos = []

follaEstilo=getSampleStyleSheet()
cabecera=follaEstilo['Heading4']
cabecera.pageBreakBefore=0
cabecera.KepWithNext=0  #Empezar pagina en blanco o no
cabecera.backColor=colors.deepskyblue

parrafo=Paragraph("OPTICA NON VES UN CARALLO", cabecera)
estilo=follaEstilo['BodyText']
cadena="Datos dos clientes: \n"
parrafo2=Paragraph(cadena,estilo)







for fila in cursor:
    tablaBaseDatos.append(fila)


titulos = [
            ["ID", "NOMBRE", "APELLIDO1", "APELLIDO2", "LOCALIDAD", "SERVIVIO"]]

clientes = titulos + tablaBaseDatos
taboa = Table(clientes)

estilo = TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightseagreen)])
taboa.setStyle(estilo)





guion = []
guion.append(parrafo)
guion.append(Spacer(0,20))
guion.append(parrafo2)
guion.append(taboa)

document = SimpleDocTemplate("Informe.pdf", pagesize=A4, showBoundary=0)
document.build(guion)
cursor.close()
bd.close()