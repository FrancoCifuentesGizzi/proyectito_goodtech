import tkinter as tk
from tkinter import ttk

class ciudad:
    #Configuración de la ventana principal
    def __init__(self, root, db):
        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry ('300x400')
        self.root.title ( "Ciudades" )
        self.root.resizable(width=0, height=0)
        self.root.transient(root)
        #Contenido Ventana
        self.__config_treeview_ciudad()
        self.__config_buttons_ciudad()

        self.root.mainloop ()

    #Configuración de las tablas y su tamaño
    def __config_treeview_ciudad(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 130, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 300)
        self.llenar_treeview_ciudades()
        self.root.after ( 0, self.llenar_treeview_ciudades )

    #Configuración de los botones
    def __config_buttons_ciudad(self):
        tk.Button(self.root, command = self.__Agregar_C, text="Agregar").place(x = 0, y = 350, width = 100, height = 50)
        tk.Button(self.root, command = self.__Editar_C, text="Editar").place(x = 100, y = 350, width = 100, height = 50)
        tk.Button(self.root, command = self.__Eliminar_C, text="Eliminar").place(x = 200, y = 350, width = 100, height = 50)

    def llenar_treeview_ciudades(self):  # Se llena el treeview de datos.
        sql = """select * from ciudad order by id_ciudad asc;"""
        # Ejecuta el select
        data = self.db.run_select ( sql )

        # Si la data es distina a la que hay actualmente...
        if (data != self.data):
            # Elimina todos los rows del treeview
            self.treeview.delete ( *self.treeview.get_children () )
            for i in data:
                self.treeview.insert ( "", "end", text=(i[0]),
                                       values= (i[1], i[1]), iid =i[0])
            self.data = data  # Actualiza la data

    def __Agregar_C(self):
        Add_Ciudad(self.db, self)

    def __Editar_C(self):
        sql = "select * from ciudad where id_ciudad = %(id_ciudad)s"
        row_data = self.db.run_select_filter ( sql, {"id_ciudad": self.treeview.focus ()} )[0]
        editar_ciudad ( self.db, self, row_data )

    def __Eliminar_C(self):
        sql = "delete from ciudad where id_ciudad = %(id_ciudad)s"
        self.db.run_sql ( sql, {"id_ciudad": self.treeview.focus ()} )
        self.llenar_treeview_ciudades ()

class Add_Ciudad:
    #Configuración de la ventana agregar
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        self.add = tk.Toplevel()
        self.add.geometry('250x90')
        self.add.title("Agregar")
        self.add.resizable(width=0, height=0)
        #Contenido Ventana
        self.__config_labels()
        self.__config_entry()
        self.__config_buttons()

    #Configuración de los labels
    def __config_labels(self):
        tk.Label(self.add ,text = "Nombre: ").place(x = 0, y = 10, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = tk.Entry(self.add)
        self.entry_nombre.place(x = 100, y = 10, width = 130, height = 20)

    #Configuración de los botones
    def __config_buttons(self):
        tk.Button(self.add, text="Aceptar",
            command = self.insertar).place ( x=75, y=45, width=105, height=25 )

    def insertar(self):  # Insercion en la base de datos.
        sql = """insert into ciudad (nombre_ciu) values (%(nombre_ciu)s)"""
        self.db.run_sql ( sql, {"nombre_ciu": self.entry_nombre.get ()} )
        self.add.destroy ()
        self.padre.llenar_treeview_ciudades ()


class editar_ciudad:  # Clase para modificar
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.insert_datos = tk.Toplevel ()
        self.config_window ()
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def config_window(self):  # Configuración de la ventana.
        self.insert_datos.geometry ( '250x110' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )


    def __config_label(self):
        tk.Label ( self.insert_datos, text= "Modificar " + (self.row_data[1]) ).place ( x=5, y=10, width=250, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=0, y=40, width=100, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = tk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=100, y=40, width=130, height=20 )
        self.entry_nombre.insert ( 0, self.row_data[1] )

        # Configuración de los botones

    def __config_button(self):
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=75, y=75, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update ciudad set nombre_ciu = %(nombre_ciu)s where id_ciudad = %(id_ciudad)s"""
        self.db.run_sql ( sql, {"nombre_ciu": self.entry_nombre.get (),
                                "id_ciudad": int ( self.row_data[0] )} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_ciudades ()

