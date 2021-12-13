import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class stock_producto:
    #Configuración de la ventana principal
    def __init__(self, root, db, b10, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b10
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview()
        self.__config_button()

    #Configuración de las tablas y su tamaño
    def __config_treeview(self):
        self.treeview = ttk.Treeview ( self.root )
        self.treeview.configure ( columns=("#0", "#1", "#2", "#3", "#4") )
        self.treeview.heading ( "#0", text="iD Producto" )
        self.treeview.heading ( "#1", text="ID Bodega" )
        self.treeview.heading ( "#2", text="Producto" )
        self.treeview.heading ( "#3", text="Bodega" )
        self.treeview.heading ( "#4", text="Stock" )
        self.treeview.column ( "#0", minwidth=10, width=90, stretch=False )
        self.treeview.column ( "#1", minwidth=10, width=90, stretch=False )
        self.treeview.column ( "#2", minwidth=60, width=200, stretch=False )
        self.treeview.column ( "#3", minwidth=30, width=215, stretch=False )
        self.treeview.column ( "#4", minwidth=30, width=60, stretch=False )
        self.treeview.place ( x=189, y=26, height=375, width=735 )
        self.llenar_treeview ()
        self.root.after ( 0, self.llenar_treeview )

    #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.treeview, text="Insertar",
                     command=self.__Agregar ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar",
                     command=self.__Editar ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar",
                     command=self.__Eliminar ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar ).place ( x=549, y=340, width=183, height=35 )

    def llenar_treeview(self):
        sql = """select producto_id_producto, bodega_id_bodega, producto.nombre_pro, bodega.nombre_bod, stock from stock_producto 
            join producto on stock_producto.producto_id_producto = producto.id_producto 
            join bodega on stock_producto.bodega_id_bodega = bodega.id_bodega
            order by producto_id_producto asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4]))
            self.data = data

    def __Agregar(self):
        Add_producto(self.db, self, self.root)

    def __Editar(self):
        if (self.treeview.focus () != ""):
            item1 = (self.treeview.item ( self.treeview.focus () ))["text"]
            item2 = (self.treeview.item ( self.treeview.focus () ))["values"]
            self.claves = [item1, item2[0]]

            sql = """select producto_id_producto, bodega_id_bodega, stock from stock_producto
            where producto_id_producto = %(producto_id_producto)s and bodega_id_bodega = %(bodega_id_bodega)s"""
            row_data = self.db.run_select_filter ( sql, {"producto_id_producto": self.claves[0], "bodega_id_bodega": self.claves[1]})[0]
            editar_producto ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                item1 = (self.treeview.item ( self.treeview.focus () ))["text"]
                item2 = (self.treeview.item ( self.treeview.focus () ))["values"]
                self.claves = [item1, item2[0]]

                sql = """delete from stock_producto where producto_id_producto = %(producto_id_producto)s 
                    and bodega_id_bodega = %(bodega_id_bodega)s"""
                self.db.run_sql ( sql, {"producto_id_producto": self.claves[0], "bodega_id_bodega": self.claves[1]})
                self.llenar_treeview ()

    def __Cerrar(self):
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
        Label(self.insert_datos ,text = "Producto: ").place(x = 10, y = 10, width = 80, height = 20)
        Label(self.insert_datos ,text = "Bodega: ").place(x = 10, y = 35, width = 80, height = 20)
        Label ( self.insert_datos, text = "Stock: " ).place ( x = 10, y=60, width=80, height=20 )

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.combo_pro = ttk.Combobox(self.insert_datos)
        self.combo_pro .place(x = 90, y = 10, width = 150, height = 20)
        self.combo_pro["values"], self.pro = self.__fill_combo_pro ()
        self.combo_bod = ttk.Combobox ( self.insert_datos )
        self.combo_bod.place ( x=90, y=35, width=150, height=20 )
        self.combo_bod["values"], self.bod = self.__fill_combo_bod ()
        self.entry_stock = ttk.Entry ( self.insert_datos )
        self.entry_stock.place ( x=90, y=60, width=150, height=20 )

        #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __fill_combo_pro(self):
        sql = "select id_producto, nombre_pro from producto order by id_producto asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_bod(self):
        sql = "select id_bodega, nombre_bod from bodega order by id_bodega asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]


    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into stock_producto (producto_id_producto, bodega_id_bodega, stock)
            values (%(id_pro)s, %(id_bod)s, %(stock)s)"""
        self.db.run_sql ( sql, {"id_pro": self.pro[self.combo_pro.current ()],
                                "id_bod": self.bod[self.combo_bod.current ()],
                                "stock": self.entry_stock.get ()} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview()

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
        Label ( self.insert_datos, text="Producto: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Bodega: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Stock: " ).place ( x=10, y=60, width=80, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.__bodega ()
        self.combo_pro = ttk.Combobox ( self.insert_datos )
        self.combo_pro.place ( x=90, y=10, width=150, height=20 )
        self.combo_pro["values"], self.pro = self.__fill_combo_pro ()
        self.combo_bod = ttk.Combobox ( self.insert_datos )
        self.combo_bod.place ( x=90, y=35, width=150, height=20 )
        self.combo_bod["values"], self.bod = self.__fill_combo_bod ()
        self.entry_stock = ttk.Entry ( self.insert_datos )
        self.entry_stock.place ( x=90, y=60, width=150, height=20 )
        self.combo_pro.insert ( 0, self.__producto () )
        self.combo_bod.insert ( 0, self.__bodega () )
        self.entry_stock.insert ( 0, self.row_data[2] )

    def __config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update stock_producto set producto_id_producto = %(id_pro)s, bodega_id_bodega = %(id_bod)s,
            stock = %(stock)s where producto_id_producto = %(producto_id_producto)s 
            and bodega_id_bodega = %(bodega_id_bodega)s"""
        self.db.run_sql ( sql, {"id_pro": self.pro[self.combo_pro.current ()],
                                "id_bod": self.bod[self.combo_bod.current ()],
                                "stock": self.entry_stock.get (),
                                "producto_id_producto": int(self.row_data[0]),
                                "bodega_id_bodega": int(self.row_data[1])})
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview ()

    def __borra(self):
        self.insert_datos.place_forget ()

    def __fill_combo_pro(self):
        sql = "select id_producto, nombre_pro from producto order by id_producto asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_bod(self):
        sql = "select id_bodega, nombre_bod from bodega order by id_bodega asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]


    def __bodega(self):
        sql = "select id_bodega, nombre_bod from bodega"
        self.datos = self.db.run_select ( sql )
        for i in self.datos:
            if i[0] == self.row_data[1]:
                return i[1]

    def __producto(self):
        sql = "select id_producto, nombre_pro from producto"
        self.datitos = self.db.run_select ( sql )
        for i in self.datitos:
            if i[0] == self.row_data[0]:
                return i[1]
