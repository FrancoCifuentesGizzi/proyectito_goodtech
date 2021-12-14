import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class stock_producto:
    #Configuración de la ventana principal
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.data = []
        self.db = db
        self.row_data = row_data
        self.detail_data = tk.Toplevel ()

        self.detail_data.geometry('735x400')
        self.detail_data.title("Detalle Bodega")
        self.detail_data.resizable(width=0, height=0)

        self.__config_treeview()
        self.__config_button()

        self.detail_data.mainloop ()

    #Configuración de las tablas y su tamaño
    def __config_treeview(self):
        self.treeview = ttk.Treeview ( self.detail_data )
        self.treeview.configure ( columns=("#0", "#1", "#2", "#3", "#4") )
        self.treeview.heading ( "#0", text="ID Producto" )
        self.treeview.heading ( "#1", text="ID Bodega" )
        self.treeview.heading ( "#2", text="Producto" )
        self.treeview.heading ( "#3", text="Bodega" )
        self.treeview.heading ( "#4", text="Stock" )
        self.treeview.column ( "#0", minwidth=10, width=90, stretch=False )
        self.treeview.column ( "#1", minwidth=10, width=90, stretch=False )
        self.treeview.column ( "#2", minwidth=60, width=200, stretch=False )
        self.treeview.column ( "#3", minwidth=30, width=215, stretch=False )
        self.treeview.column ( "#4", minwidth=30, width=60, stretch=False )
        self.treeview.place ( x=0, y=0, height=375, width=735 )
        self.llenar_treeview ()
        self.detail_data.after ( 0, self.llenar_treeview )

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
        Add_producto(self.db, self, self.detail_data, self.row_data)

    def __Editar(self):
        if (self.treeview.focus () != ""):
            item1 = (self.treeview.item ( self.treeview.focus () ))["text"]
            item2 = (self.treeview.item ( self.treeview.focus () ))["values"]
            self.claves = [item1, item2[0]]

            sql = """select producto_id_producto, bodega_id_bodega, stock from stock_producto
            where producto_id_producto = %(producto_id_producto)s and bodega_id_bodega = %(bodega_id_bodega)s"""
            rowerer_data = self.db.run_select_filter ( sql, {"producto_id_producto": self.claves[0], "bodega_id_bodega": self.claves[1]})[0]
            if rowerer_data[1] == self.row_data[0]:
                editar_producto ( self.db, self, rowerer_data, self.detail_data, self.row_data )
                pass
        else:
            messagebox.showinfo ( self.detail_data, message="Seleccione un objeto de la lista" )

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
        self.detail_data.destroy ()
        self.__limpia_pantalla ()

class Add_producto:
    #Configuración de la ventana agregar
    def __init__(self, db, padre, insert_datos, row_data):
        self.padre = padre
        self.db = db
        self.insert_datos = insert_datos
        self.row_data = row_data

        self.insert_datos = tk.Toplevel()
        self.insert_datos.geometry('210x165')
        self.insert_datos.title("Agregar")
        self.insert_datos.resizable(width=0, height=0)

        self.__config_label()
        self.__config_entry()
        self.__config_button()

    #Configuración de los labels
    def __config_label(self):
        Label(self.insert_datos, text = "Producto: ").place(x = 10, y = 10, width = 80, height = 20)
        Label(self.insert_datos, text = "Stock: " ).place ( x = 10, y=35, width=80, height=20 )

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.combo_pro = ttk.Combobox(self.insert_datos)
        self.combo_pro .place(x = 90, y = 10, width = 100, height = 20)
        self.combo_pro["values"], self.pro = self.__fill_combo_pro ()
        self.entry_stock = ttk.Entry ( self.insert_datos )
        self.entry_stock.place ( x=90, y=35, width=100, height=20 )

        #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.__insertar ).place ( x=0, y=100, width=70, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=140, y=100, width=70, height=30 )

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
                                "id_bod": self.row_data[0],
                                "stock": self.entry_stock.get ()} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview()

    def __borra(self):
        self.insert_datos.destroy ()

class editar_producto:  # Clase para modificar
    def __init__(self, db, padre, rowerer_data, edit_datos, row_data):
        self.padre = padre
        self.db = db
        self.rowerer_data = rowerer_data
        self.row_data = row_data
        self.edit_datos = edit_datos

        self.edit_datos = tk.Toplevel()
        self.edit_datos.geometry('210x165')
        self.edit_datos.title("Agregar")
        self.edit_datos.resizable(width=0, height=0)

        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):
        Label ( self.edit_datos, text="Producto: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.edit_datos, text="Stock: " ).place ( x=10, y=35, width=80, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.combo_pro = ttk.Combobox ( self.edit_datos )
        self.combo_pro.place ( x=90, y=10, width=100, height=20 )
        self.combo_pro["values"], self.pro = self.__fill_combo_pro ()
        self.entry_stock = ttk.Entry ( self.edit_datos )
        self.entry_stock.place ( x=90, y=35, width=100, height=20 )
        self.combo_pro.insert ( 0, self.__producto () )
        self.entry_stock.insert ( 0, self.rowerer_data[2] )

    def __config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        ttk.Button ( self.edit_datos, text="Aceptar",
                    command=self.modificar ).place ( x=0, y=100, width=70, height=30 )
        ttk.Button ( self.edit_datos, text="Cancelar",
                     command=self.__borra ).place ( x=140, y=100, width=70, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update stock_producto set producto_id_producto = %(id_pro)s,
            stock = %(stock)s where producto_id_producto = %(producto_id_producto)s
            and bodega_id_bodega = %(bodega_id_bodega)s"""
        self.db.run_sql ( sql, {"id_pro": self.pro[self.combo_pro.current ()],
                                "stock": self.entry_stock.get (),
                                "producto_id_producto": int(self.rowerer_data[0]),
                                "bodega_id_bodega": int(self.row_data[0])})
        self.edit_datos.destroy ()
        self.padre.llenar_treeview ()

    def __borra(self):
        self.edit_datos.destroy ()

    def __fill_combo_pro(self):
        sql = "select id_producto, nombre_pro from producto order by id_producto asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __producto(self):
        sql = "select id_producto, nombre_pro from producto"
        self.datitos = self.db.run_select ( sql )
        for i in self.datitos:
            if i[0] == self.row_data[0]:
                return i[1]
