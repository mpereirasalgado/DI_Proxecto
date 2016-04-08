from gi.repository import Gtk
import sqlite3 as dbapi

from reportlab.platypus import Paragraph, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

"""  Creando la conexino a la base de datos.  """

# version de api
from gi.repository.NetworkManager import ConnectionError

print(dbapi.apilevel)
# nivel de seuridade de fios de 0 a 3
print(dbapi.threadsafety)
# insercion de param
print(dbapi.paramstyle)
"""  Comprobando la conexión.  """
try:
    bd = dbapi.connect("e.dat")
except (ConnectionError, dbapi.DatabaseError):
    print("Error de conexion")
else:
    print("Conexion establecida")
finally:
    print("Conexion lista")

"""  Creación de la tabla clientes.  """

cursor = bd.cursor()

crearTablaClientes = """create table if not exists clientes(
ID int primary key,
NOMBRE text not null,
APELLIDO1 text not null,
APELLIDO2 text not null,
LOCALIDAD text not null,
SERVICIO text not null)
"""

cursor.execute(crearTablaClientes)
bd.commit()

ID = "0"
NOMBRE = "VACIO"
APELLIDO1 = "VACIO"
APELLIDO2 = "VACIO"
LOCALIDAD = "VACIO"
SERVICIO = "VACIO"

"""  Creacion de ventana.  """

class StackWindow(Gtk.Window):
    """  Clase generadora de la aplicacion.
    """
    def __init__(self):
        """  Inicializador de la clase StackWindow.
        """
        Gtk.Window.__init__(self, title="OPTICA NO VES UN CARAJO")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        self.add(vbox)

        """  creacion del stack tendra 3 elementos INICIO GESTION INFO.  """
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)


        texto = Gtk.Label()
        texto.set_text("PROXECTO OPTICA NO VES UN CARAJO POR ESO ESTAS AQUI\n"
                       "\n"
                       "\nVER INFORMACION PARA EL CORRECTO FUNCIONAMIENTO EN INFO")
        stack.add_titled(texto, "inicio", "INICIO")



        """  creacion de un notebook dentro del segundo elemento del stack, el notebook tendra 3 elementos, INSERTAR VER MODIFICAR.  """
        notebook = Gtk.Notebook()


        """  elemento insertar donde creamos una tabla para colocar labels y entrys ademas lo hago scrollable por si no me cabe en pantalla  """
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


        table = Gtk.Table(9, 3, True)

        texto1 = Gtk.Label(label="ID")
        texto2 = Gtk.Label(label="NOMBRE")
        texto3 = Gtk.Label(label="PRIMER APELLIDO")
        texto4 = Gtk.Label(label="SEGUNDO APELLIDO")
        texto5 = Gtk.Label(label="LOCALIDAD")
        texto6 = Gtk.Label(label="SERVICIO")
        texto7 = Gtk.Label(label="los servicios disponibles son:")
        texto8 = Gtk.Label(label="revision  lentillas  gafas  arreglo")

        self.entry1 = Gtk.Entry()
        self.entry2 = Gtk.Entry()
        self.entry3 = Gtk.Entry()
        self.entry4 = Gtk.Entry()
        self.entry5 = Gtk.Entry()
        self.entry6 = Gtk.Entry()

        button = Gtk.Button(label="INSERTAR")
        button.connect("clicked", self.insertar)

        """  colocacion en la tabla de los labels y los entrys  """
        table.attach(texto1, 0, 1, 0, 1)
        table.attach(self.entry1, 2, 3, 0, 1)
        table.attach(texto2, 0, 1, 1, 2)
        table.attach(self.entry2, 2, 3, 1, 2)
        table.attach(texto3, 0, 1, 2, 3)
        table.attach(self.entry3, 2, 3, 2, 3)
        table.attach(texto4, 0, 1, 3, 4)
        table.attach(self.entry4, 2, 3, 3, 4)
        table.attach(texto5, 0, 1, 4, 5)
        table.attach(self.entry5, 2, 3, 4, 5)
        table.attach(texto6, 0, 1, 5, 6)
        table.attach(self.entry6, 2, 3, 5, 6)
        table.attach(texto7, 0, 1, 6, 7)
        table.attach(texto8, 2, 3, 6, 7)
        table.attach(button, 0, 3, 8, 9)


        scrolled.add(table)

        notebook.append_page(scrolled, Gtk.Label('INSERTAR CLIENTES'))

        """  creamos un grid para posicionar bien el treeView y los botones.  """
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        """  guardado de datos de la tabla clientes para luego insertarlos en el treeView.   """
        cursor.execute("""select * from clientes""")

        resultados = cursor.fetchall()

        """  guardamos los datos en una lista  """
        self.servicios_liststore = Gtk.ListStore(int, str, str, str, str, str)
        for servicios_ref in resultados:
                    self.servicios_liststore.append(list(servicios_ref))

        """  en la aplicacion podemos filtrar los clientes por servicios  """
        """  aqui ponemos ese filtro en None por defecto para que muestre todos los datos.  """
        self.current_filter_servicio = None

        """  creamos el filtro.  """
        self.servicio_filter = self.servicios_liststore.filter_new()
        """  ponemos la funcion al filtro.  """
        self.servicio_filter.set_visible_func(self.servicio_filter_func)

        """  creamos el treeView y le ponemos como modelo el filtro creado anteriormente.  """
        treeview = Gtk.TreeView.new_with_model(self.servicio_filter)
        for i, column_title in enumerate(["ID", "NOMBRE", "APELLIDO1", "APELLIDO2", "LOCALIDAD", "SERVICIO"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            treeview.append_column(column)

        """  creacion de la lista de botones con los que filtraremos los clientes por cada servicio.  """
        buttons = list()
        for prog_servicio in ["gafas", "lentillas", "revision", "arreglo", "nada", ]:
            button = Gtk.Button(prog_servicio)
            bactu = Gtk.Button(label= "ACTUALIZAR")
            bgen = Gtk.Button(label= "GENERAR")
            buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)
            bactu.connect("clicked", self.actualizar)
            bgen.connect("clicked", self.generar)

        """  un scroll para el treeView.  """
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        grid.attach(scrollable_treelist, 0, 0, 8, 11)
        grid.attach_next_to(buttons[0], scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(bactu, buttons[0], Gtk.PositionType.BOTTOM, 8, 1)
        grid.attach_next_to(bgen, bactu, Gtk.PositionType.BOTTOM, 8, 1)
        for i, button in enumerate(buttons[1:]):
            grid.attach_next_to(button, buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        scrollable_treelist.add(treeview)

        notebook.append_page(grid, Gtk.Label('VER TABLA DE CLIENTES'))

        """  tercer elemento del notebook donde podremos modificar datos.  """
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


        table = Gtk.Table(9, 4, True)

        texto1 = Gtk.Label(label="ID")
        texto2 = Gtk.Label(label="NOMBRE")
        texto3 = Gtk.Label(label="PRIMER APELLIDO")
        texto4 = Gtk.Label(label="SEGUNDO APELLIDO")
        texto5 = Gtk.Label(label="LOCALIDAD")
        texto6 = Gtk.Label(label="SERVICIO")
        texto7 = Gtk.Label(label="los servicios disponibles son:")
        texto8 = Gtk.Label(label="revision  lentillas  gafas  arreglo")

        self.entry11 = Gtk.Entry()
        self.entry22 = Gtk.Entry()
        self.entry33 = Gtk.Entry()
        self.entry44 = Gtk.Entry()
        self.entry55 = Gtk.Entry()
        self.entry66 = Gtk.Entry()

        button1 = Gtk.Button(label="MODIFICAR")
        button1.connect("clicked", self.modificar)
        button2 = Gtk.Button(label="BORRAR")
        button2.connect("clicked", self.borrar)

        table.attach(texto1, 0, 1, 0, 1)
        table.attach(self.entry11, 2, 3, 0, 1)
        table.attach(button2, 3, 4, 0, 1)
        table.attach(texto2, 0, 1, 1, 2)
        table.attach(self.entry22, 2, 3, 1, 2)
        table.attach(texto3, 0, 1, 2, 3)
        table.attach(self.entry33, 2, 3, 2, 3)
        table.attach(texto4, 0, 1, 3, 4)
        table.attach(self.entry44, 2, 3, 3, 4)
        table.attach(texto5, 0, 1, 4, 5)
        table.attach(self.entry55, 2, 3, 4, 5)
        table.attach(texto6, 0, 1, 5, 6)
        table.attach(self.entry66, 2, 3, 5, 6)
        table.attach(texto7, 0, 1, 6, 7)
        table.attach(texto8, 2, 3, 6, 7)
        table.attach(button1, 0, 4, 8, 9)

        scroll.add(table)

        notebook.append_page(scroll, Gtk.Label('MODIFICAR CLIENTES'))

        stack.add_titled(notebook, "gestion", "GESTION")

        texto = Gtk.Label()
        texto.set_text("INFORMACION ADICIONAL\n\n"
                       "\tLos botones debajo de la tabla son para filtrar los clientes por servicios\n\n"
                       "\tA corregir en proximas versiones\n\n"
                       "\t\tdebo poner un combobox tanto al insertar como al modificar para introducir los servicios")
        stack.add_titled(texto, "info", "INFO")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.props.valign = Gtk.Align.CENTER

        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)



    def servicio_filter_func(self, model, iter, data):
        """ metodo de comprobación del filtro.
        :param model:
        :param iter:
        :param data:
        :return:
        """
        if self.current_filter_servicio is None or self.current_filter_servicio == "nada":
            return True
        else:
            return model[iter][5] == self.current_filter_servicio
    #al pulsar los botones de filtro
    def on_selection_button_clicked(self, widget):
        """ controla lo que pasa al pulsar sobre un boton de filtrado.
        :param widget:
        :return:
        """

        self.current_filter_servicio = widget.get_label()
        print("%s servicio sseleccionado!" % self.current_filter_servicio)

        self.servicio_filter.refilter()
    #insertar datos en la tabla y treeview
    def insertar(self, button):
        """ metodo para insertar nuevos clientes en la base de datos.
        :param self:
        :param button:
        :return:
        """
        ID = self.entry1.get_text()
        NOMBRE = self.entry2.get_text()
        APELLIDO1 = self.entry3.get_text()
        APELLIDO2= self.entry4.get_text()
        LOCALIDAD= self.entry5.get_text()
        SERVICIO= self.entry6.get_text()
        print(ID + " " + NOMBRE + " " + APELLIDO1 + " " + APELLIDO2 + " " + LOCALIDAD + " " + SERVICIO + " ")
        insertarDatos = """insert into clientes values(
        '""" + ID + """',
        '""" + NOMBRE + """',
        '""" + APELLIDO1 + """',
        '""" + APELLIDO2 + """',
        '""" + LOCALIDAD + """',
        '""" + SERVICIO + """'
        )"""

        cursor.execute(insertarDatos)
        bd.commit()
        cursor.execute("""select * from clientes""")
        bd.commit
        for result in cursor:
            print("ID:" + str(result[0]) + " NOMBRE:" + result[1] + " APELLIDO1: " + result[2]+ " APELLIDO2: " + result[3]+ " LOCALIDAD: " + result[4]+ " SERVICIO: " + result[5])

        self.servicios_liststore.append(list(result))


    #borrar cliente de la tabla
    def borrar(self, Button):
        """ metodo para borrar clientes de la base de datos.
        :param self:
        :param Button:
        :return:
        """

        ID = self.entry11.get_text()
        cursor = bd.cursor()
        try:
            cursor.execute("""delete from clientes where ID='"""+ID+"""'""")
            bd.commit()
            print("borrado")
        except:
            bd.rollback()


    #modificar datos de clientes
    def modificar(self, Button):
        """ metodo para modificar los datos de un cliente existente.
        :param self:
        :param Button:
        :return:
        """
        ID = self.entry11.get_text()
        NOMBRE = self.entry22.get_text()
        APELLIDO1 = self.entry33.get_text()
        APELLIDO2= self.entry44.get_text()
        LOCALIDAD= self.entry55.get_text()
        SERVICIO= self.entry66.get_text()
        cursor = bd.cursor()

        try:
            cursor.execute("""update clientes set
                                 ID='""" + ID + """',
                                 NOMBRE='""" + NOMBRE + """',
                                 APELLIDO1='""" + APELLIDO1 + """',
                                 APELLIDO2='""" + APELLIDO2 + """',
                                 LOCALIDAD='""" + LOCALIDAD + """',
                                 SERVICIO='""" + SERVICIO + """'
                                 where ID ='""" + ID + """'
                                 """)
            bd.commit()
            print("modificado")
        except:
            bd.rollback()

    #actualizar el treeview para ver las modificaciones
    def actualizar(self, Button):
        """ metodo que actualiza la base de datos.
        :param self:
        :param Button:
        :return:
        """

        cursor = bd.cursor()
        self.servicios_liststore.clear()
        cursor.execute("select * from clientes")
        resultado = cursor.fetchall()
        bd.commit()
        for res in resultado:
            self.servicios_liststore.append(res)

    def generar(self, Button):


        cursor = bd.cursor()

        cursor.execute("select * from clientes")
        resultado = cursor.fetchall()

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


        for fila in resultado:
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

        document = SimpleDocTemplate("a ver si vas.pdf", pagesize=A4, showBoundary=0)
        document.build(guion)
        cursor.close()


win = StackWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()