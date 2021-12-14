import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class perfil:
    #Configuración de la ventana principal
    def __init__(self, root, db, b10, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b10
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_perfil()
        self.__config_buttons_perfil()

    #Configuración de las tablas y su tamaño
    def __config_treeview_perfil(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Tipo")
        self.treeview.column("#0", minwidth = 100, width = 200, stretch = False)
        self.treeview.column("#1", minwidth = 130, width = 200, stretch = False)
        self.treeview.place(x = 370, y = 26, height = 375, width = 400)
        self.llenar_treeview_perfil()
        self.root.after ( 0, self.llenar_treeview_perfil )

    #Configuración de los botones
    def __config_buttons_perfil(self):
        ttk.Button ( self.treeview, command=self.__Agregar_Pe,
                     text="Agregar" ).place ( x=0, y=340, width=100, height=35 )
        ttk.Button ( self.treeview, command=self.__Editar_Pe,
                     text="Editar" ).place ( x=100, y=340, width=100, height=35 )
        ttk.Button ( self.treeview, command=self.__Eliminar_Pe,
                     text="Eliminar" ).place ( x=200, y=340, width=100, height=35 )
        ttk.Button ( self.treeview, command=self.__Cerrar_Pe,
                     text="Cerrar" ).place ( x=300, y=340, width=100, height=35 )


    def llenar_treeview_perfil(self):  # Se llena el treeview de datos.
        sql = """select * from perfil order by id_perfil asc;"""
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

    def __Agregar_Pe(self):
        Add_Perfil(self.db, self, self.root)

    def __Editar_Pe(self):
        if (self.treeview.focus () != ""):
            sql = "select * from perfil where id_perfil = %(id_perfil)s"
            row_data = self.db.run_select_filter ( sql, {"id_perfil": self.treeview.focus ()} )[0]
            editar_perfil ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )


    def __Eliminar_Pe(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = "delete from perfil where id_perfil = %(id_perfil)s"
                self.db.run_sql ( sql, {"id_perfil": self.treeview.focus ()} )
                self.llenar_treeview_perfil ()

    def __Cerrar_Pe(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla()

class Add_Perfil:
    #Configuración de la ventana agregar
    def __init__(self, db, padre, root):
        self.padre = padre
        self.db = db
        self.root = root

        self.__config_labels()
        self.__config_entry()
        self.__config_button()

    #Configuración de los labels
    def __config_labels(self):
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        ttk.Label(self.insert_datos ,text = "Tipo: ").place(x = 10, y = 35, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_tipo = tk.Entry(self.insert_datos)
        self.entry_tipo.place(x = 90, y = 35, width = 150, height = 20)

    #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def insertar(self):  # Insercion en la base de datos.
        sql = """insert into perfil (tipo_perfil) values (%(tipo_perfil)s)"""
        self.db.run_sql ( sql, {"tipo_perfil": self.entry_tipo.get ()} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_perfil ()

    def __borra(self):
        self.insert_datos.place_forget ()

class editar_perfil:  # Clase para modificar
    def __init__(self, db, padre, row_data, root):
        self.padre = padre
        self.db = db
        self.root = root
        self.row_data = row_data
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        ttk.Label ( self.insert_datos, text="Tipo: " ).place ( x=10, y=35, width=90, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_tipo = ttk.Entry ( self.insert_datos )
        self.entry_tipo.place ( x=90, y=35, width=150, height=20 )
        self.entry_tipo.insert ( 0, self.row_data[1] )

        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update perfil set tipo_perfil = %(tipo_perfil)s where id_perfil = %(id_perfil)s"""
        self.db.run_sql ( sql, {"tipo_perfil": self.entry_tipo.get (),
                                "id_perfil": int ( self.row_data[0] )} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_perfil ()

    def __borra(self):
        self.insert_datos.place_forget ()