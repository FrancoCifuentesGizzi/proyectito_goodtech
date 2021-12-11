import tkinter as tk
from tkinter import ttk

class perfil:
    #Configuración de la ventana principal
    def __init__(self, root, db):
        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry ('300x400')
        self.root.title ( "Perfiles" )
        self.root.resizable(width=0, height=0)
        self.root.transient(root)
        #Contenido Ventana
        self.__config_treeview_perfil()
        self.__config_buttons_perfil()

        self.root.mainloop ()

    #Configuración de las tablas y su tamaño
    def __config_treeview_perfil(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Tipo")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 130, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 300)
        self.llenar_treeview_perfil()
        self.root.after ( 0, self.llenar_treeview_perfil )

    #Configuración de los botones
    def __config_buttons_perfil(self):
        ttk.Button(self.root, command = self.__Agregar_Pe, text="Agregar").place(x = 0, y = 350, width = 100, height = 50)
        ttk.Button(self.root, command = self.__Editar_Pe, text="Editar").place(x = 100, y = 350, width = 100, height = 50)
        ttk.Button(self.root, command = self.__Eliminar_Pe, text="Eliminar").place(x = 200, y = 350, width = 100, height = 50)

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
        Add_Perfil(self.db, self)

    def __Editar_Pe(self):
        sql = "select * from perfil where id_perfil = %(id_perfil)s"
        row_data = self.db.run_select_filter ( sql, {"id_perfil": self.treeview.focus ()} )[0]
        editar_perfil ( self.db, self, row_data )


    def __Eliminar_Pe(self):
        sql = "select * from perfil where id_perfil = %(id_perfil)s"
        row_data = self.db.run_select_filter ( sql, {"id_perfil": self.treeview.focus ()} )[0]
        Eliminar_Perfil( self.db, self, row_data )



class Add_Perfil:
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
        tk.Label(self.add ,text = "Tipo: ").place(x = 0, y = 10, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_tipo = tk.Entry(self.add)
        self.entry_tipo.place(x = 100, y = 10, width = 130, height = 20)

    #Configuración de los botones
    def __config_buttons(self):
        ttk.Button(self.add, text="Aceptar",
            command = self.insertar).place ( x=75, y=45, width=105, height=25 )

    def insertar(self):  # Insercion en la base de datos.
        sql = """insert into perfil (tipo_perfil) values (%(tipo_perfil)s)"""
        self.db.run_sql ( sql, {"tipo_perfil": self.entry_tipo.get ()} )
        self.add.destroy ()
        self.padre.llenar_treeview_perfil ()


class editar_perfil:  # Clase para modificar
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
        tk.Label ( self.insert_datos, text="Tipo: " ).place ( x=0, y=40, width=100, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_tipo = ttk.Entry ( self.insert_datos )
        self.entry_tipo.place ( x=100, y=40, width=130, height=20 )
        self.entry_tipo.insert ( 0, self.row_data[1] )

        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar", command=self.modificar ).place ( x=75, y=75, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update perfil set tipo_perfil = %(tipo_perfil)s where id_perfil = %(id_perfil)s"""
        self.db.run_sql ( sql, {"tipo_perfil": self.entry_tipo.get (),
                                "id_perfil": int ( self.row_data[0] )} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_perfil ()

# Clase para eliminar
class Eliminar_Perfil:
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.del_datos = tk.Toplevel ()
        self.config_window ()
        self.__config_label ()
        self.__config_button ()

    # Configuración de la ventana
    def config_window(self):
        self.del_datos.geometry ( '250x130' )
        self.del_datos.title ( "Eliminando datos" )
        self.del_datos.resizable ( width=0, height=0 )

    def __config_label(self):
        tk.Label ( self.del_datos, text= "Se eliminará los siguientes datos: ").place ( x=5, y=10, width=250, height=20 )
        tk.Label ( self.del_datos, text= "Nombre: " + (self.row_data[1])).place( x=5, y=30, width=250, height=20 )
    def __config_button(self):
        ttk.Button(self.del_datos, command = self.__Cancelar, text="Cancelar").place(x = 0, y = 80, width = 100, height = 50)
        ttk.Button(self.del_datos, command = self.__Aceptar, text="Aceptar").place(x = 150, y = 80, width = 100, height = 50)

    def __Cancelar(self):
        self.del_datos.destroy()

    def __Aceptar(self):
        sql = "delete from perfil where id_perfil = %(id_perfil)s"
        self.db.run_sql ( sql, {"id_perfil": int ( self.row_data[0] )} )
        self.del_datos.destroy ()
        self.padre.llenar_treeview_perfil ()
