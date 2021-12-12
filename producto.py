import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class producto:
    #Configuración de la ventana principal
    def __init__(self, root, db, b6, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b6
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_producto()
        self.__config_buttons_producto()


    #Configuración de las tablas y su tamaño
    def __config_treeview_producto(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Precio")
        self.treeview.heading("#3", text = "Marca")

        self.treeview.column("#0", minwidth = 30, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 30, width = 235, stretch = False)
        self.treeview.column("#2", minwidth = 30, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 30, width = 200, stretch = False)
        self.treeview.place(x = 189, y = 26, height = 375, width = 735)
        self.llenar_treeview_producto ()
        self.root.after ( 0, self.llenar_treeview_producto)

    #Configuración de los botones
    def __config_buttons_producto(self):
        ttk.Button ( self.treeview, text="Insertar Producto",
                     command=self.__Agregar_P ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar Producto",
                     command=self.__Editar_P ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Producto",
                     command=self.__Eliminar_P ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_P ).place ( x=549, y=340, width=183, height=35 )

    def llenar_treeview_producto(self):
        sql = """select id_producto, nombre_pro, precio_pro, marca.nombre_marca
            from producto join marca on producto.marca_id_marca = marca.id_marca order by id_producto asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3]), iid=i[0])
            self.data = data

    def __Agregar_P(self):
        Add_producto(self.db, self, self.root)

    def __Editar_P(self):
        if (self.treeview.focus () != ""):
            sql = """select id_producto, nombre_pro, precio_pro, marca.nombre_marca from producto 
                join marca on producto.marca_id_marca = marca.id_marca where id_producto = %(id_producto)s"""
            row_data = self.db.run_select_filter ( sql, {"id_producto": self.treeview.focus ()} )[0]
            editar_producto ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar_P(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = """delete from producto where id_producto = %(id_producto)s"""
                self.db.run_sql ( sql, {"id_producto": self.treeview.focus ()} )
                self.llenar_treeview_producto ()

    def __Cerrar_P(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()

class Add_producto:
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
        Label(self.insert_datos ,text = "Precio: ").place(x = 10, y = 35, width = 80, height = 20)
        Label(self.insert_datos ,text = "Marca: ").place(x = 10, y = 60, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_precio = ttk.Entry(self.insert_datos)
        self.entry_precio.place(x = 90, y = 35, width = 150, height = 20)
        self.combo_marca = ttk.Combobox(self.insert_datos)
        self.combo_marca.place(x = 90, y = 60, width = 150, height = 20)
        self.combo_marca["values"], self.marca = self.__fill_combo_marca ()

        #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __fill_combo_marca(self):
        sql = "select id_marca, nombre_marca from marca order by id_marca"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into producto (nombre_pro, precio_pro, marca_id_marca)
            values (%(nombre_pro)s, %(precio_pro)s, %(marca_id_marca)s)"""
        self.db.run_sql ( sql, {"nombre_pro": self.entry_nombre.get (),
                                "precio_pro": self.entry_precio.get (),
                                "marca_id_marca": self.marca[self.combo_marca.current ()]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_producto()

    def __borra(self):
        self.insert_datos.place_forget ()

class editar_producto:  # Clase para modificar
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
        Label ( self.insert_datos, text="Precio: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Marca: " ).place ( x=10, y=60, width=80, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 90, y = 10, width = 150, height = 20)
        self.entry_precio = ttk.Entry(self.insert_datos)
        self.entry_precio.place(x = 90, y = 35, width = 150, height = 20)
        self.combo_marca = ttk.Combobox(self.insert_datos)
        self.combo_marca.place(x = 90, y = 60, width = 150, height = 20)
        self.combo_marca["values"], self.marca = self.__fill_combo_marca ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_precio.insert ( 0, self.row_data[2] )
        self.combo_marca.insert ( 0, self.row_data[3] )

    def __config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update producto set nombre_pro = %(nombre_pro)s, precio_pro = %(precio_pro)s,
            marca_id_marca = %(id_marca)s where id_producto = %(id_producto)s"""
        self.db.run_sql ( sql, {"nombre_pro": self.entry_nombre.get (),
                                "precio_pro": self.entry_precio.get (),
                                "id_marca": self.marca[self.combo_marca.current ()],
                                "id_producto": self.row_data[0]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_producto ()

    def __borra(self):
        self.insert_datos.place_forget ()

    def __fill_combo_marca(self):
        sql = "select id_marca, nombre_marca from marca"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

