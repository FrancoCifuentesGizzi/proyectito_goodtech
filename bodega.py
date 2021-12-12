import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class bodega:
    #Configuración de la ventana principal
    def __init__(self, root, db, b4, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b4
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_bodega()
        self.__config_buttons_bodega()

    #Configuración de las tablas y su tamaño
    def __config_treeview_bodega(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Direccion")
        self.treeview.heading("#3", text = "Telefono")
        self.treeview.heading("#4", text = "Ciudad")
        self.treeview.column("#0", minwidth = 30, width = 70, stretch = False)
        self.treeview.column("#1", minwidth = 40, width = 165, stretch = False)
        self.treeview.column("#2", minwidth = 40, width = 165, stretch = False)
        self.treeview.column("#3", minwidth = 40, width = 165, stretch = False)
        self.treeview.column("#4", minwidth = 40, width = 165, stretch = False)
        self.treeview.place(x = 189, y = 26, height = 375, width = 735)
        self.llenar_treeview_bodega ()
        self.root.after ( 0, self.llenar_treeview_bodega)

    #Configuración de los botones
    def __config_buttons_bodega(self):
        ttk.Button ( self.treeview, text="Agregar Bodega",
                     command=self.__Agregar_B ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar Bodega",
                     command=self.__Editar_B ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Bodega",
                     command=self.__Eliminar_B ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_B ).place ( x=549, y=340, width=183, height=35 )

    def llenar_treeview_bodega(self):
        sql = """select id_bodega, nombre_bod, direccion_bod, telefono_bod, ciudad.nombre_ciu
           from bodega join ciudad on bodega.ciudad_id_ciudad = ciudad.id_ciudad order by id_bodega asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4]), iid=i[0])
            self.data = data


    def __Agregar_B(self):
        Add_bodega(self.db, self, self.root)

    def __Editar_B(self):
        if (self.treeview.focus () != ""):
            sql = "select id_bodega, nombre_bod, direccion_bod, telefono_bod, ciudad.nombre_ciu from bodega " \
                  "join ciudad on bodega.ciudad_id_ciudad = ciudad.id_ciudad where id_bodega = %(id_bodega)s"
            row_data = self.db.run_select_filter ( sql, {"id_bodega": self.treeview.focus ()} )[0]
            editar_bodega ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar_B(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = """delete from bodega where id_bodega = %(id_bodega)s"""
                self.db.run_sql ( sql, {"id_bodega": self.treeview.focus ()} )
                self.llenar_treeview_bodega ()

    def __Cerrar_B(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()

class Add_bodega:
    #Configuración de la ventana agregar
    def __init__(self, db, padre, root):
        self.padre = padre
        self.db = db
        self.root = root
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    #Configuración de los labels
    def __config_label(self):
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        Label(self.insert_datos ,text = "Nombre: ").place(x = 10, y = 10, width = 80, height = 20)
        Label(self.insert_datos ,text = "Direccion: ").place(x = 10, y = 35, width = 80, height = 20)
        Label(self.insert_datos ,text = "Telefono: ").place(x = 10, y = 60, width = 80, height = 20)
        Label(self.insert_datos ,text = "Ciudad: ").place(x = 270, y = 10, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_direccion = ttk.Entry(self.insert_datos)
        self.entry_direccion.place(x = 90, y = 35, width = 150, height = 20)
        self.entry_telefono = ttk.Entry(self.insert_datos)
        self.entry_telefono.place(x = 90, y = 60, width = 150, height = 20)
        self.combo_ciudad = ttk.Combobox(self.insert_datos)
        self.combo_ciudad.place(x = 340, y = 10, width = 150, height = 20)
        self.combo_ciudad["values"], self.ids = self.__fill_combo ()

        #Configuración de los botones
    def __config_button(self):  # Se configura el boton
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __fill_combo(self):
        sql = """select id_ciudad, nombre_ciu from ciudad order by id_ciudad asc"""
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into bodega (nombre_bod, direccion_bod, telefono_bod, ciudad_id_ciudad )
            values (%(nombre_bod)s, %(direccion_bod)s, %(telefono_bod)s, %(ciudad_id_ciudad)s)"""
        self.db.run_sql ( sql, {"nombre_bod": self.entry_nombre.get (),
                                "direccion_bod": self.entry_direccion.get (),
                                "telefono_bod": self.entry_telefono.get (),
                                "ciudad_id_ciudad": self.ids[self.combo_ciudad.current ()]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_bodega()

    def __borra(self):
        self.insert_datos.place_forget ()


class editar_bodega:  # Clase para modificar
    def __init__(self, db, padre, row_data, root):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.root = root
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Direccion: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Telefono: " ).place ( x=10, y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Ciudad: " ).place ( x=270, y=10, width=80, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_direccion = ttk.Entry(self.insert_datos)
        self.entry_direccion.place(x = 90, y = 35, width = 150, height = 20)
        self.entry_telefono = ttk.Entry(self.insert_datos)
        self.entry_telefono.place(x = 90, y = 60, width = 150, height = 20)
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 340, y = 10, width = 150, height = 20)
        self.combo["values"], self.ids = self.fill_combo ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_direccion.insert ( 0, self.row_data[2] )
        self.entry_telefono.insert ( 0, self.row_data[3] )
        self.combo.insert ( 0, self.row_data[4] )

    def __config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update bodega set nombre_bod = %(nombre_bod)s, direccion_bod = %(direccion_bod)s,
                telefono_bod = %(telefono_bod)s, ciudad_id_ciudad = %(id_ciudad)s
                where id_bodega = %(id_bodega)s"""
        self.db.run_sql ( sql, {"nombre_bod": self.entry_nombre.get (),
                                "direccion_bod": self.entry_direccion.get (),
                                "telefono_bod": self.entry_telefono.get (),
                                "id_ciudad": self.ids[self.combo.current ()],
                                "id_bodega": self.row_data[0]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_bodega ()

    def fill_combo(self):  #
        sql = "select id_ciudad, nombre_ciu from ciudad order by id_ciudad asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __borra(self):
        self.insert_datos.place_forget ()
