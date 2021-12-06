import tkinter as tk
from tkinter import ttk

class cliente:  # Clase de equipo, puede llamar a las clases de insertar y modificar
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel ()
        self.root.geometry ( '740x400' )
        self.root.title ( "Clientes" )
        # toplevel modal
        self.root.transient ( root )

        #
        self.__config_treeview_cliente ()
        self.__config_buttons_cliente ()

    def __config_treeview_cliente(self):  # Se configura el treeview
        self.treeview = ttk.Treeview ( self.root )
        self.treeview.configure ( columns=("#0", "#1", "#2", "#3", "#4") )
        self.treeview.heading ( "#0", text="RUT" )
        self.treeview.heading ( "#1", text="Nombre" )
        self.treeview.heading ( "#2", text="Apellido" )
        self.treeview.heading ( "#3", text="Dirección" )
        self.treeview.heading ( "#4", text="Teléfono" )
        self.treeview.column ( "#0", minwidth=50, width=120, stretch=False )
        self.treeview.column ( "#1", minwidth=275, width=150, stretch=False )
        self.treeview.column ( "#2", minwidth=275, width=150, stretch=False )
        self.treeview.column ( "#3", minwidth=275, width=200, stretch=False )
        self.treeview.column ( "#4", minwidth=275, width=120, stretch=False )
        self.treeview.place ( x=0, y=0, height=350, width=740 )
        self.llenar_treeview_cliente()
        self.root.after(0, self.llenar_treeview_cliente)

    def __config_buttons_cliente(self):  # Botones de insertar, modificar y eliminar
        tk.Button ( self.root, text="Insertar Cliente",
                    command=self.insertar_cliente ).place ( x=0, y=350, width=246, height=50 )
        tk.Button ( self.root, text="Modificar Cliente",
                    command=self.modificar_cliente ).place ( x=246, y=350, width=246, height=50 )
        tk.Button ( self.root, text="Eliminar Cliente",
                    command=self.eliminar_cliente ).place ( x=492, y=350, width=246, height=50 )

    def llenar_treeview_cliente(self):  # Se llena el treeview de datos.
        sql = "select * from cliente order by id_cliente asc"
        # Ejecuta el select
        data = self.db.run_select ( sql )

        # Si la data es distina a la que hay actualmente...
        if (data != self.data):
            # Elimina todos los rows del treeview
            self.treeview.delete ( *self.treeview.get_children () )
            for i in data:
                # Inserta los datos
                self.treeview.insert ( "", "end", text=i[1],
                                       values=(i[2], i[3], i[4], i[5]), iid=i[1] )
            self.data = data  # Actualiza la data

    def insertar_cliente(self):
        insertar_cliente( self.db, self )

    def modificar_cliente(self):
        sql = "select * from cliente where rut_cliente = %(rut_cliente)s"
        row_data = self.db.run_select_filter ( sql, {"rut_cliente": self.treeview.focus ()} )[0]
        modificar_cliente ( self.db, self, row_data )

    def eliminar_cliente(self):
        sql = "delete from cliente where rut_cliente = %(rut_cliente)s"
        self.db.run_sql ( sql, {"rut_cliente": self.treeview.focus ()} )
        self.llenar_treeview_cliente ()


class insertar_cliente:  # Clase para insertar data
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db
        self.insert_datos = tk.Toplevel ()
        self.__config_window ()
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_window(self):  # Settings
        self.insert_datos.geometry ( '270x250' )
        self.insert_datos.title ( "Insertar Cliente" )
        self.insert_datos.resizable ( width=0, height=0 )

    def __config_label(self):  # Labels
        tk.Label ( self.insert_datos, text="RUT: " ).place ( x=10, y=10, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=40, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=70, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Dirección: " ).place ( x=10, y=100, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Teléfono: " ).place ( x=10, y=130, width=80, height=20 )

    def __config_entry(self):  # Se configuran los inputs
        self.entry_rut = tk.Entry ( self.insert_datos )
        self.entry_rut.place ( x=110, y=10, width=150, height=20 )
        self.entry_nombre = tk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=110, y=40, width=150, height=20 )
        self.entry_apellido = tk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=110, y=70, width=150, height=20 )
        self.entry_direccion = tk.Entry ( self.insert_datos )
        self.entry_direccion.place ( x=110, y=100, width=150, height=20 )
        self.entry_telefono = tk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=110, y=130, width=150, height=20 )

    def __config_button(self):  # Se configura el boton
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=35, y=200, width=200, height=30 )

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into cliente (rut_cliente, nombre_cli, apellido_cli, direccion_cli, telefono_cli) 
                values (%(rut_cliente)s, %(nombre_cli)s, %(apellido_cli)s, %(direccion_cli)s, %(telefono_cli)s)"""
        self.db.run_sql ( sql, {"rut_cliente": self.entry_rut.get (),
                                "nombre_cli": self.entry_nombre.get (),
                                "apellido_cli": self.entry_apellido.get (),
                                "direccion_cli": self.entry_direccion.get (),
                                "telefono_cli": self.entry_telefono.get () } )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_cliente ()


class modificar_cliente:  # Clase para modificar
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.insert_datos = tk.Toplevel ()
        self.config_window ()
        self.config_label ()
        self.config_entry ()
        self.config_button ()

    def config_window(self):  # Configuración de la ventana.
        self.insert_datos.geometry ( '270x250' )
        self.insert_datos.title ( "Modificar Cliente" )
        self.insert_datos.resizable ( width=0, height=0 )

    def config_label(self):  # Se configuran las etiquetas.
        tk.Label ( self.insert_datos, text= " Rut de cliente: " + (self.row_data[1]) ).place ( x=35, y=10, width=200, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=40, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=70, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Dirección: " ).place ( x=10, y=100, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Teléfono: " ).place ( x=10, y=130, width=80, height=20 )

    def config_entry(self):  # Se configuran los inputs
        self.entry_nombre = tk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=110, y=40, width=150, height=20 )
        self.entry_apellido = tk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=110, y=70, width=150, height=20 )
        self.entry_direccion = tk.Entry ( self.insert_datos )
        self.entry_direccion.place ( x=110, y=100, width=150, height=20 )
        self.entry_telefono = tk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=110, y=130, width=150, height=20 )
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_apellido.insert ( 0, self.row_data[2] )
        self.entry_direccion.insert ( 0, self.row_data[3] )
        self.entry_telefono.insert ( 0, self.row_data[4] )




    def config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=35, y=190, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update cliente set nombre_cli = %(nombre_cli)s, apellido_cli = %(apellido_cli)s, direccion_cli = %(direccion_cli)s, telefono_cli = %(telefono_cli)s
                where rut_cliente = %(rut_cliente)s"""
        self.db.run_sql ( sql, {"nombre_cli": self.entry_nombre.get(),
                                "apellido_cli": self.entry_apellido.get(),
                                "direccion_cli": self.entry_direccion.get(),
                                "telefono_cli": self.entry_telefono.get(),
                                "rut_cliente": self.row_data[1]} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_cliente ()