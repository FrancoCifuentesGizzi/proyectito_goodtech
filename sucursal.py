import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class sucursal:
    #Configuración de la ventana principal
    def __init__(self, root, db, b2, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b2
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_sucursales()
        self.__config_buttons_sucursal()


    #Configuración de las tablas y su tamaño
    def __config_treeview_sucursales(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4", "#5"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Direccion")
        self.treeview.heading("#3", text = "Telefono")
        self.treeview.heading("#4", text = "Ciudad")
        self.treeview.heading("#5", text = "Bodega")
        self.treeview.column("#0", minwidth = 30, width = 60, stretch = False)
        self.treeview.column("#1", minwidth = 50, width = 135, stretch = False)
        self.treeview.column("#2", minwidth = 50, width = 135, stretch = False)
        self.treeview.column("#3", minwidth = 50, width = 135, stretch = False)
        self.treeview.column("#4", minwidth = 50, width = 135, stretch = False)
        self.treeview.column("#5", minwidth = 50, width = 135, stretch = False)
        self.treeview.place(x = 189, y = 26, height = 375, width = 735)
        self.llenar_treeview_sucursal ()
        self.root.after ( 0, self.llenar_treeview_sucursal )

    #Configuración de los botones
    def __config_buttons_sucursal(self):
        ttk.Button ( self.treeview, text="Agregar Sucursal",
                     command=self.__Agregar_S ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar Sucursal",
                     command=self.__Editar_S ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Sucursal",
                     command=self.__Eliminar_S ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_S ).place ( x=549, y=340, width=183, height=35 )

    def llenar_treeview_sucursal(self):
        sql = """select id_sucursal, nombre_suc, direccion_suc, telefono_suc, ciudad.nombre_ciu, bodega.nombre_bod 
           from sucursal join ciudad on sucursal.ciudad_id_ciudad = ciudad.id_ciudad 
           join bodega on sucursal.bodega_id_bodega = bodega.id_bodega order by id_sucursal asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5]), iid=i[0] )
            self.data = data


    def __Agregar_S(self):
        Add_Sucursal(self.db, self, self.root)

    def __Editar_S(self):
        if (self.treeview.focus () != ""):
            sql = """select id_sucursal, nombre_suc, direccion_suc, telefono_suc, ciudad.nombre_ciu, bodega.nombre_bod from sucursal 
                join ciudad on sucursal.ciudad_id_ciudad = ciudad.id_ciudad 
                join bodega on sucursal.bodega_id_bodega = bodega.id_bodega where id_sucursal = %(id_sucursal)s"""
            row_data = self.db.run_select_filter ( sql, {"id_sucursal": self.treeview.focus ()} )[0]
            editar_sucursal ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar_S(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = """delete from sucursal where id_sucursal = %(id_sucursal)s"""
                self.db.run_sql ( sql, {"id_sucursal": self.treeview.focus ()} )
                self.llenar_treeview_sucursal ()

    def __Cerrar_S(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()

class Add_Sucursal:
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
        Label(self.insert_datos, text = "Nombre: ").place(x = 10, y = 10, width = 80, height = 20)
        Label(self.insert_datos, text = "Direccion: ").place(x = 10, y = 35, width = 80, height = 20)
        Label(self.insert_datos, text = "Telefono: ").place(x = 10, y = 60, width = 80, height = 20)
        Label(self.insert_datos, text = "Ciudad: ").place(x = 270, y = 10, width = 80, height = 20)
        Label(self.insert_datos, text = "Bodega: ").place(x = 270, y = 35, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_direccion = ttk.Entry(self.insert_datos)
        self.entry_direccion.place(x =90, y = 35, width = 150, height = 20)
        self.entry_telefono = ttk.Entry(self.insert_datos)
        self.entry_telefono.place(x =90, y = 60, width = 150, height = 20)
        self.combociudad = ttk.Combobox(self.insert_datos)
        self.combociudad.place(x = 340, y = 10, width = 150, height = 20)
        self.combociudad["values"], self.city = self.__fill_combo_ciudad ()
        self.combobodega = ttk.Combobox(self.insert_datos)
        self.combobodega.place(x = 340, y = 35, width = 150, height = 20)
        self.combobodega["values"], self.alm = self.__fill_combo_bodega ()

        #Configuración de los botones
    def __config_button(self):  # Se configura el boton
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __fill_combo_ciudad(self):
        sql = "select id_ciudad, nombre_ciu from ciudad order by id_ciudad asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_bodega(self):
        sql = "select id_bodega, nombre_bod from bodega order by id_bodega asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert sucursal (nombre_suc, direccion_suc, telefono_suc, ciudad_id_ciudad, bodega_id_bodega ) 
            values (%(nombre_suc)s, %(direccion_suc)s, %(telefono_suc)s, %(ciudad_id_ciudad)s, %(bodega_id_bodega)s);"""
        self.db.run_sql ( sql, {"nombre_suc": self.entry_nombre.get (),
                                "direccion_suc": self.entry_direccion.get (),
                                "telefono_suc": self.entry_telefono.get (),
                                "ciudad_id_ciudad": self.city[self.combociudad.current ()],
                                "bodega_id_bodega": self.alm[self.combobodega.current ()]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_sucursal ()

    def __borra(self):
        self.insert_datos.place_forget ()


class editar_sucursal:  # Clase para modificar
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
        Label ( self.insert_datos, text="Bodega: " ).place ( x=270, y=35, width=80, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_direccion = ttk.Entry(self.insert_datos)
        self.entry_direccion.place(x = 90, y = 35, width = 150, height = 20)
        self.entry_telefono = ttk.Entry(self.insert_datos)
        self.entry_telefono.place(x = 90, y = 60, width = 150, height = 20)
        self.combociudad = ttk.Combobox(self.insert_datos)
        self.combociudad.place(x = 340, y = 10, width = 150, height = 20)
        self.combociudad["values"], self.city = self.fill_combo_ciudad ()
        self.combobodega = ttk.Combobox ( self.insert_datos )
        self.combobodega.place ( x=340, y=35, width=150, height=20 )
        self.combobodega["values"], self.alm = self.fill_combo_bodega ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_direccion.insert ( 0, self.row_data[2] )
        self.entry_telefono.insert ( 0, self.row_data[3] )
        self.combociudad.insert ( 0, self.row_data[4] )
        self.combobodega.insert ( 0, self.row_data[5] )
        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update sucursal set nombre_suc = %(nombre_suc)s, direccion_suc = %(direccion_suc)s, 
                telefono_suc = %(telefono_suc)s, ciudad_id_ciudad = %(id_ciudad)s, bodega_id_bodega = %(id_bodega)s
                where id_sucursal = %(id_sucursal)s"""
        self.db.run_sql ( sql, {"nombre_suc": self.entry_nombre.get (),
                                "direccion_suc": self.entry_direccion.get (),
                                "telefono_suc": self.entry_telefono.get (),
                                "id_ciudad": self.city[self.combociudad.current ()],
                                "id_bodega": self.alm[self.combobodega.current ()],
                                "id_sucursal": self.row_data[0]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_sucursal ()

    def fill_combo_ciudad(self):  #
        sql = "select id_ciudad, nombre_ciu from ciudad order by id_ciudad asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def fill_combo_bodega(self):  #
        sql = "select id_bodega, nombre_bod from bodega order by id_bodega asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __borra(self):
        self.insert_datos.place_forget ()
