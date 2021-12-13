import tkinter as tk
from tkinter import ttk

class detalle:
    #Configuración de la ventana principal
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.data = []
        self.db = db
        self.row_data = row_data
        self.detail_data = tk.Toplevel ()

        self.detail_data.geometry('700x400')
        self.detail_data.title("Detalle Venta")
        self.detail_data.resizable(width=0, height=0)

        self.__config_treeview_detalles()
        self.__config_buttons_detalles()

        self.detail_data.mainloop ()

    #Configuración de las tablas y su tamaño
    def __config_treeview_detalles(self):
        self.treeview = ttk.Treeview(self.detail_data)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3"))
        self.treeview.heading("#0", text = "Producto")
        self.treeview.heading("#1", text = "Id Venta")
        self.treeview.heading("#2", text = "Precio Unitario")
        self.treeview.heading("#3", text = "Cantidad")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#2", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 200, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        self.llenar_treeview_detalle ()
        self.detail_data.after ( 0, self.llenar_treeview_detalle )

    #Configuración de los botones
    def __config_buttons_detalles(self):
        ttk.Button(self.detail_data, command = self.__Agregar_PV, text="Agregar Producto").place(x = 0, y = 350, width = 275, height = 50)
        # ttk.Button(self.detail_data, command = self.__Eliminar_PV, text="Eliminar Producto").place(x = 275, y = 350, width = 275, height = 50)

    def llenar_treeview_detalle(self):
        sql = """select nombre_pro, id_venta, precio_venta, cantidad from detalle_venta
            join producto on detalle_venta.producto_id_producto = producto.id_producto
            join venta on detalle_venta.venta_id_venta = venta.id_venta order by id_venta asc"""
        data = self.db.run_select (sql)

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3]), iid=i[0] )
            self.data = data

    def __Agregar_PV(self):
        Add_ProVent(self.db, self, self.row_data)
        self.padre.llenar_treeview_venta ()

    # def __Eliminar_PV(self):
    #     sql = "select * from detalle_venta where (producto_id_producto = %(producto_id_producto)s AND venta_id_venta = %(venta_id_venta)s)"
    #     rowerer_data = self.db.run_select_filter ( sql, {"producto_id_producto": self.treeview.focus (), "venta_id_venta": self.treeview.o} )[0]
    #     Del_ProVent(self.db, self, rowerer_data, row_data)

class Add_ProVent:
    #Configuración de la ventana agregar
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data

        self.add = tk.Toplevel()
        self.add.geometry('210x165')
        self.add.title("Agregar")
        self.add.resizable(width=0, height=0)
        #Contenido Ventana
        self.__config_labels()
        self.__config_entry()
        self.__config_buttons()

    #Configuración de los labels
    def __config_labels(self):
        tk.Label(self.add ,text = "Producto: ").place(x = 0, y = 10, width = 100, height = 20)
        tk.Label(self.add ,text = "Precio: ").place(x = 0, y = 35, width = 100, height = 20)
        tk.Label(self.add ,text = "Cantidad: ").place(x = 0, y = 60, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.comboproducto = ttk.Combobox(self.add)
        self.comboproducto.place(x = 100, y = 10, width = 100, height = 20)
        self.comboproducto["values"], self.pro = self.__fill_combo_pro ()
        self.entry_precio = ttk.Entry(self.add)
        self.entry_precio.place(x = 100, y = 35, width = 100, height = 20)
        self.entry_cantidad = ttk.Entry(self.add)
        self.entry_cantidad.place(x = 100, y = 60, width = 100, height = 20)

        #Configuración de los botones
    def __config_buttons(self):
        ttk.Button(self.add, text="Aceptar",
                  command = self.__insertar).place(x = 55, y = 120, width = 105, height = 30)

    def __fill_combo_pro(self):
        sql = "select id_producto, nombre_pro from producto order by id_producto asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert detalle_venta (producto_id_producto, venta_id_venta, precio_venta, cantidad)
            values (%(producto_id_producto)s, %(venta_id_venta)s, %(precio_venta)s, %(cantidad)s);"""
        self.db.run_sql ( sql, {"producto_id_producto": self.pro[self.comboproducto.current ()],
                                "venta_id_venta": self.row_data[0],
                                "precio_venta": self.entry_precio.get (),
                                "cantidad": self.entry_cantidad.get ()})

        sql = """call ProductoIn(%(cantidad)s, %(precio)s, %(current)s);"""
        self.db.run_sql ( sql, {"cantidad": self.entry_cantidad.get(),
                                "precio": self.entry_precio.get(),
                                "current": self.row_data[0]})
        self.add.destroy ()
        self.padre.llenar_treeview_detalle ()
