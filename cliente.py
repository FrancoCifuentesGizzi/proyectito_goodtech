import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class cliente:  # Clase de equipo, puede llamar a las clases de insertar y modificar
    def __init__(self, root, db, b1, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b1
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

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
        self.treeview.column ( "#0", minwidth=30, width=100, stretch=False )
        self.treeview.column ( "#1", minwidth=30, width=150, stretch=False )
        self.treeview.column ( "#2", minwidth=30, width=150, stretch=False )
        self.treeview.column ( "#3", minwidth=30, width=200, stretch=False )
        self.treeview.column ( "#4", minwidth=30, width=130, stretch=False )
        self.treeview.place ( x=189, y=26, height=375, width=735 )
        self.llenar_treeview_cliente()
        self.root.after(0, self.llenar_treeview_cliente)

    def __config_buttons_cliente(self):  # Botones de insertar, modificar y eliminar
        ttk.Button ( self.treeview, text="Insertar Cliente",
                     command=self.insertar_cliente ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar Cliente",
                     command=self.modificar_cliente ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Cliente",
                     command=self.eliminar_cliente ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.cerrar_cliente ).place ( x=549, y=340, width=183, height=35 )

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
        insertar_cliente( self.db, self, self.root )

    def modificar_cliente(self):
        if (self.treeview.focus () != ""):
            sql = "select * from cliente where rut_cliente = %(rut_cliente)s"
            row_data = self.db.run_select_filter ( sql, {"rut_cliente": self.treeview.focus ()} )[0]
            modificar_cliente ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def eliminar_cliente(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?")
            if (ke_dijo == True):
                sql = "delete from cliente where rut_cliente = %(rut_cliente)s"
                self.db.run_sql ( sql, {"rut_cliente": self.treeview.focus ()} )
                self.llenar_treeview_cliente ()

    def cerrar_cliente(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()



class insertar_cliente:  # Clase para insertar data
    def __init__(self, db, padre, root):
        self.padre = padre
        self.db = db
        self.root = root
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):  # Labels
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        Label ( self.insert_datos, text="RUT: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Apellido: " ).place ( x=10 , y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Dirección: " ).place ( x=270, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Teléfono: " ).place ( x=270, y=35, width=80, height=20 )

    def __config_entry(self):  # Se configuran los inputs
        self.entry_rut = ttk.Entry ( self.insert_datos )
        self.entry_rut.place ( x=90, y=10, width=150, height=20 )
        self.entry_nombre = ttk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=90, y=35, width=150, height=20 )
        self.entry_apellido = ttk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=90, y=60, width=150, height=20 )
        self.entry_direccion = ttk.Entry ( self.insert_datos )
        self.entry_direccion.place ( x=340, y=10, width=150, height=20 )
        self.entry_telefono = ttk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=340, y=35, width=150, height=20 )

    def __config_button(self):  # Se configura el boton
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )

        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into cliente (rut_cliente, nombre_cli, apellido_cli, direccion_cli, telefono_cli) 
                values (%(rut_cliente)s, %(nombre_cli)s, %(apellido_cli)s, %(direccion_cli)s, %(telefono_cli)s)"""
        self.db.run_sql ( sql, {"rut_cliente": self.entry_rut.get (),
                                "nombre_cli": self.entry_nombre.get (),
                                "apellido_cli": self.entry_apellido.get (),
                                "direccion_cli": self.entry_direccion.get (),
                                "telefono_cli": self.entry_telefono.get () } )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_cliente ()

    def __borra(self):
        self.insert_datos.place_forget ()


class modificar_cliente:  # Clase para modificar
    def __init__(self, db, padre, row_data, root):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.root = root

        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):  # Se configuran las etiquetas.
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        Label ( self.insert_datos, text= " Rut de cliente: " + (self.row_data[1]) ).place ( x=10, y=10, width= 200, height=20 )
        Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Dirección: " ).place ( x=270, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Teléfono: " ).place ( x=270, y=35, width=80, height=20 )

    def __config_entry(self):  # Se configuran los inputs
        self.entry_nombre = ttk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=90, y=35, width=150, height=20 )
        self.entry_apellido = ttk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=90, y=60, width=150, height=20 )
        self.entry_direccion = ttk.Entry ( self.insert_datos )
        self.entry_direccion.place ( x=340, y=10, width=150, height=20 )
        self.entry_telefono = ttk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=340, y=35, width=150, height=20 )
        self.entry_nombre.insert ( 0, self.row_data[2] )
        self.entry_apellido.insert ( 0, self.row_data[3] )
        self.entry_direccion.insert ( 0, self.row_data[4] )
        self.entry_telefono.insert ( 0, self.row_data[5] )


    def __config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update cliente set nombre_cli = %(nombre_cli)s, apellido_cli = %(apellido_cli)s, direccion_cli = %(direccion_cli)s, telefono_cli = %(telefono_cli)s
                where rut_cliente = %(rut_cliente)s"""
        self.db.run_sql ( sql, {"nombre_cli": self.entry_nombre.get(),
                                "apellido_cli": self.entry_apellido.get(),
                                "direccion_cli": self.entry_direccion.get(),
                                "telefono_cli": self.entry_telefono.get(),
                                "rut_cliente": self.row_data[1]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_cliente ()

    def __borra(self):
        self.insert_datos.place_forget ()