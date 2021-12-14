import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox
from tkcalendar import DateEntry

class venta:
    #Configuración de la ventana principal
    def __init__(self, root, db, b8, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b8
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_venta()
        self.__config_buttons_venta()


    #Configuración de las tablas y su tamaño
    def __config_treeview_venta(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4", "#5"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Fecha")
        self.treeview.heading("#2", text = "Sucursal")
        self.treeview.heading("#3", text = "Empleado")
        self.treeview.heading("#4", text = "Cliente")
        self.treeview.heading("#5", text = "Total")
        self.treeview.column ( "#0", minwidth=20, width=60, stretch=False )
        self.treeview.column ( "#1", minwidth=50, width=120, stretch=False )
        self.treeview.column ( "#2", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#3", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#4", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#5", minwidth=50, width=135, stretch=False )
        self.treeview.place ( x=189, y=26, height=270, width=735 )
        self.llenar_treeview_venta ()
        self.root.after ( 0, self.llenar_treeview_venta )

    #Configuración de los botones
    def __config_buttons_venta(self):
        ttk.Button(self.treeview, text="Agregar Venta",
                   command = self.__Agregar_V).place(x = 0, y = 235, width = 147, height = 35)
        ttk.Button(self.treeview, text="Modificar Venta",
                   command = self.__Editar_V).place(x = 147, y = 235, width = 147, height = 35)
        ttk.Button(self.treeview, text="Detalles de Venta",
                   command = self.__Editar_D).place(x = 294, y = 235, width = 147, height = 35)
        ttk.Button(self.treeview, text="Eliminar Venta",
                   command = self.__Eliminar_V).place(x = 441, y = 235, width = 147, height = 35)
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_V ).place ( x = 588, y = 235, width = 147, height = 35 )

    def llenar_treeview_venta(self):
        sql = """select id_venta, fecha, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli, total  from venta
            join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
            join empleado on venta.empleado_id_empleado = empleado.id_empleado
            join cliente on venta.cliente_id_cliente = cliente.id_cliente order by id_venta asc"""
        data = self.db.run_select ( sql )
        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(str(i[1]), i[2], i[3], i[4], i[5]), iid=i[0] )
            self.data = data

    def __Agregar_V(self):
        Add_Venta(self.db, self, self.root)

    def __Editar_V(self):
        if (self.treeview.focus () != ""):
            sql = """select id_venta, fecha, total, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli from venta
                join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
                join empleado on venta.empleado_id_empleado = empleado.id_empleado
                join cliente on venta.cliente_id_cliente = cliente.id_cliente where id_venta = %(id_venta)s"""
            row_data = self.db.run_select_filter ( sql, {"id_venta": self.treeview.focus ()} )[0]

            editar_venta ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Editar_D(self):
        if (self.treeview.focus () != ""):
            sql = """select id_venta, fecha, total, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli from venta
                join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
                join empleado on venta.empleado_id_empleado = empleado.id_empleado
                join cliente on venta.cliente_id_cliente = cliente.id_cliente where id_venta = %(id_venta)s"""
            self.row_data = self.db.run_select_filter ( sql, {"id_venta": self.treeview.focus ()} )[0]
            self.dato = (self.treeview.focus ())
            detalle ( self.db, self, self.root, self.dato, self.row_data, self.llenar_treeview_venta )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar_V(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = "delete from venta where id_venta = %(id_venta)s"
                self.db.run_sql ( sql, {"id_venta": self.treeview.focus ()} )
                self.llenar_treeview_venta()

    def __Cerrar_V(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()

class Add_Venta:
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
        self.insert_datos = LabelFrame ( self.root, text="Ingreso" )
        self.insert_datos.place ( x=189, y=300, width=735, height=120 )
        Label(self.insert_datos ,text = "Fecha: ").place(x = 10, y = 10, width = 80, height = 20)
        Label(self.insert_datos ,text = "Sucursal: ").place(x = 10, y = 35, width = 80, height = 20)
        Label(self.insert_datos ,text = "Empleado: ").place(x = 10, y = 60, width = 80, height = 20)
        Label(self.insert_datos ,text = "Cliente: ").place(x = 270, y = 10, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_fecha = DateEntry ( self.insert_datos, selectmode='day' )
        self.entry_fecha.place ( x=90, y=10, width=150, height=20 )
        self.combosucursal = ttk.Combobox(self.insert_datos)
        self.combosucursal.place(x = 90, y = 35, width = 150, height = 20)
        self.combosucursal["values"], self.suc = self.__fill_combo_suc ()

        self.combocliente = ttk.Combobox(self.insert_datos)
        self.combocliente.place(x = 340, y = 10, width = 150, height = 20)
        self.combocliente["values"], self.client = self.__fill_combo_client ()

        #Configuración de los botones
    def __config_button(self):  # Se configura el boton
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )
        ttk.Button ( self.insert_datos, text=">>>",
                     command=self._employer).place ( x=242, y=30, width=35, height=30 )

    def __fill_combo_suc(self):
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]


    def _employer (self):
        self.comboempleado = ttk.Combobox(self.insert_datos)
        self.comboempleado.place(x = 90, y = 60, width = 150, height = 20)
        self.comboempleado["values"], self.wrk = self.__fill_combo_wrk ()

    def __fill_combo_wrk(self):
        sql = """select id_empleado, nombre_emp from empleado 
        where sucursal_id_sucursal = %(id_suc)s order by id_empleado asc"""
        self.data = self.db.run_select_filter ( sql, {"id_suc": self.suc[self.combosucursal.current ()]} )

        return [i[1] for i in self.data], [i[0] for i in self.data]


    def __fill_combo_client(self):
        sql = "select id_cliente, nombre_cli from cliente order by id_cliente asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert venta (fecha, total, sucursal_id_sucursal, empleado_id_empleado, cliente_id_cliente )
            values (%(fecha)s, %(total)s, %(sucursal_id_sucursal)s, %(empleado_id_empleado)s, %(cliente_id_cliente)s);"""
        self.db.run_sql ( sql, {"fecha": self.entry_fecha.get_date (),
                                "total": 0,
                                "sucursal_id_sucursal": self.suc[self.combosucursal.current ()],
                                "empleado_id_empleado": self.wrk[self.comboempleado.current ()],
                                "cliente_id_cliente": self.client[self.combocliente.current ()]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_venta ()

    def __borra(self):
        self.insert_datos.place_forget ()

class editar_venta:  # Clase para modificar
    def __init__(self, db, padre, row_data, root):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.root = root

        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_label(self):
        self.insert_datos = ttk.LabelFrame ( self.root, text="Modificación" )
        self.insert_datos.place ( x=189, y=300, width=735, height=120 )
        Label ( self.insert_datos, text="Fecha: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Sucursal: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Empleado: " ).place ( x=10, y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Cliente: " ).place ( x=270, y=10, width=80, height=20 )

# Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_fecha = DateEntry ( self.insert_datos, selectmode='day' )
        self.entry_fecha.place ( x=90, y=10, width=150, height=20 )
        self.combosucursal = ttk.Combobox ( self.insert_datos )
        self.combosucursal.place ( x=90, y=35, width=150, height=20 )
        self.combosucursal["values"], self.suc = self.__fill_combo_suc ()
        self.comboempleado = ttk.Combobox ( self.insert_datos )
        self.comboempleado.place ( x=90, y=60, width=150, height=20 )
        self.comboempleado["values"], self.wrk = self.__fill_combo_wrk ()
        self.combocliente = ttk.Combobox ( self.insert_datos )
        self.combocliente.place ( x=340, y=10, width=150, height=20 )
        self.combocliente["values"], self.client = self.__fill_combo_client ()
        self.combosucursal.insert ( 0, self.row_data[3] )
        self.comboempleado.insert ( 0, self.row_data[4] )
        self.combocliente.insert ( 0, self.row_data[5] )

        # Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update venta set fecha = %(fecha)s, sucursal_id_sucursal = %(id_sucursal)s,
                empleado_id_empleado = %(id_empleado)s, cliente_id_cliente = %(id_cliente)s
                where id_venta = %(id_venta)s"""
        self.db.run_sql ( sql, {"fecha": self.entry_fecha.get_date (),
                                "id_sucursal": self.suc[self.combosucursal.current ()],
                                "id_empleado": self.wrk[self.comboempleado.current ()],
                                "id_cliente": self.client[self.combocliente.current ()],
                                "id_venta": self.row_data[0]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_venta ()

    def __fill_combo_suc(self):  #
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_wrk(self):  #
        sql = "select id_empleado, nombre_emp from empleado order by id_empleado asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]
    def __fill_combo_client(self):  #
        sql = "select id_cliente, nombre_cli from cliente order by id_cliente asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __borra(self):
        self.insert_datos.place_forget ()


class detalle:
    #Configuración de la ventana principal
    def __init__(self, db, padre, root, dato, row_data, llenar_treeview_venta):
        self.padre = padre
        self.data_detalle = []
        self.db = db
        self.dato = dato
        self.row_data = row_data
        self.root = root
        self.llenar_venta = llenar_treeview_venta

        self.__config_treeview_detalles()
        self.__config_buttons_detalles()

    #Configuración de las tablas y su tamaño
    def __config_treeview_detalles(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Producto")
        self.treeview.heading("#2", text="Id Venta" )
        self.treeview.heading("#3", text = "Precio unitario")
        self.treeview.heading("#4", text = "Cantidad")
        self.treeview.column("#0", minwidth = 30, width = 50, stretch = False)
        self.treeview.column("#1", minwidth = 30, width = 190, stretch = False)
        self.treeview.column("#2", minwidth = 50, width = 50, stretch = False)
        self.treeview.column("#3", minwidth = 50, width = 120, stretch = False)
        self.treeview.column ("#4", minwidth=200, width=70, stretch=False )
        self.treeview.place(x = 189, y = 300, height = 225, width = 480)
        self.llenar_treeview_detalle ()
        self.root.after ( 0, self.llenar_treeview_detalle )

    #Configuración de los botones
    def __config_buttons_detalles(self):
        ttk.Button ( self.treeview, text="Agregar Producto",
                     command=self.__Agregar_PV ).place ( x=0, y=190, width=120, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Producto",
                     command=self.__Eliminar_PV ).place ( x=120, y=190, width=120, height=35 )
        ttk.Button ( self.treeview, text="Actualizar",
                     command=self.__Aceptar_PV ).place ( x=240, y=190, width=120, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_PV ).place ( x=360, y=190, width=120, height=35 )

    def llenar_treeview_detalle(self):
        sql = """select id_detalle, nombre_pro, id_venta, precio_venta, cantidad from detalle_venta
            join producto on detalle_venta.producto_id_producto = producto.id_producto
            join venta on detalle_venta.venta_id_venta = venta.id_venta where detalle_venta.venta_id_venta = %(id_venta)s order by id_detalle asc"""
        data_detalle = self.db.run_select_filter ( sql, {"id_venta": self.dato} )

        if (data_detalle != self.data_detalle):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data_detalle:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4]), iid=i[0] )
            self.data_detalle = data_detalle

    def __Agregar_PV(self):
        Add_ProVent(self.db, self, self.root, self.row_data, self.dato)

    def __Eliminar_PV(self):
        if (self.treeview.focus () != ""):
            sql = "select * from detalle_venta where id_detalle = %(id_detalle)s"
            self.rowerer_data = self.db.run_select_filter ( sql, {"id_detalle": self.treeview.focus ()} )[0]
            if self.rowerer_data[2] == self.row_data[0]:
                ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
                if (ke_dijo == True):
                    sql = "delete from detalle_venta where id_detalle = %(id_detalle)s"
                    self.db.run_sql ( sql, {"id_detalle": self.rowerer_data[0]} )

                    sql = """call ProductoOut(%(cantidad)s, %(precio)s, %(current)s);"""
                    self.db.run_sql ( sql, {"cantidad": self.rowerer_data[4],
                                "precio": self.rowerer_data[3],
                                "current": self.row_data[0]} )
                    self.llenar_treeview_detalle ()

    def __Aceptar_PV(self):
        self.padre.llenar_treeview_venta ()

    def __Cerrar_PV(self):
        self.treeview.place_forget ()


class Add_ProVent:
    #Configuración de la ventana agregar
    def __init__(self, db, padre, root, row_data, dato):
        self.padre = padre
        self.db = db
        self.root = root
        self.row_data = row_data
        self.dato = dato
        self._sucursal()

        #Contenido Ventana
        self.__config_labels()
        self.__config_entry()
        self.__config_buttons()

    #Configuración de los labels
    def __config_labels(self):
        self.insert_datos = LabelFrame ( self.root, text="Ingreso de producto" )
        self.insert_datos.place ( x=675, y=300, width=250, height=225 )
        tk.Label(self.insert_datos ,text = "Producto: ").place(x = 10, y = 10, width = 80, height = 20)
        tk.Label(self.insert_datos ,text = "Precio venta: ").place(x = 10, y = 70, width = 80, height = 20)
        tk.Label(self.insert_datos ,text = "Cantidad: ").place(x = 10, y = 95, width = 80, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.comboproducto = ttk.Combobox(self.insert_datos)
        self.comboproducto.place(x = 90, y = 10, width = 130, height = 20)
        self.comboproducto["values"], self.pro = self._produ ()
        self.entry_precio = ttk.Entry(self.insert_datos)
        self.entry_precio.place(x = 90, y = 70, width = 130, height = 20)
        self.entry_cantidad = ttk.Entry(self.insert_datos)
        self.entry_cantidad.place(x = 90, y = 95, width = 130, height = 20)


        #Configuración de los botones
    def __config_buttons(self):
        ttk.Button ( self.insert_datos, text="Ver precio",
                     command=self.__precio ).place ( x=90, y=36, width=105, height=30 )
        ttk.Button(self.insert_datos, text="Aceptar",
                  command = self.__insertar).place(x = 60, y = 140, width = 105, height = 30)
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=60, y=175, width=105, height=30 )



    def _sucursal(self):
        sql = "select id_venta, sucursal_id_sucursal from venta order by id_venta asc"
        datitos = self.db.run_select ( sql )
        for i in datitos:
            if i[0] == (int(self.dato)):
                self.id_sucu = i[1]
        self._bodega()

    def _bodega(self):
        sql = "select id_sucursal, bodega_id_bodega from sucursal order by id_sucursal asc"
        datito = self.db.run_select ( sql )
        for i in datito:
            if i[0] == (int (self.id_sucu)):
                self.id_bode = i[1]
        self._produ ()

    def _produ(self):
        sql = """select producto_id_producto, producto.nombre_pro from stock_producto 
              inner join producto on stock_producto.producto_id_producto = producto.id_producto 
              where bodega_id_bodega = %(id_bode)s order by producto_id_producto asc"""
        self.data = self.db.run_select_filter ( sql, {"id_bode": self.id_bode} )
        return [i[1] for i in self.data], [i[0] for i in self.data]


    def __precio(self):
        sql = "select id_producto, precio_pro from producto order by id_producto asc"
        self.datitos = self.db.run_select (sql)
        for i in self.datitos:
            if i[0] == (self.pro[self.comboproducto.current ()]):
                self.entry_precio.delete(0, "end")
                self.entry_precio.insert(0, i[1])

    def __borra(self):
        self.insert_datos.place_forget ()

    def __insertar(self):  # Insercion en la base de datos.
        if int(self.entry_precio.get()) > 0:
            if int(self.entry_cantidad.get ()) > 0 :
                sql = """insert detalle_venta (producto_id_producto, venta_id_venta, precio_venta, cantidad)
                            values (%(producto_id_producto)s, %(venta_id_venta)s, %(precio_venta)s, %(cantidad)s);"""
                self.res = self.db.run_sql ( sql, {"producto_id_producto": self.pro[self.comboproducto.current ()],
                                                   "venta_id_venta": self.row_data[0],
                                                   "precio_venta": self.entry_precio.get (),
                                                   "cantidad": self.entry_cantidad.get ()} )
                sql = """call ProductoIn(%(cantidad)s, %(precio)s, %(current)s);"""
                self.db.run_sql ( sql, {"cantidad": self.entry_cantidad.get(),
                                    "precio": self.entry_precio.get(),
                                    "current": self.row_data[0]})

                proce_stock = """call desc_stock (%(id_pro)s, %(id_bod)s, %(cantidad)s)"""
                self.db.run_sql ( proce_stock, {"id_pro": self.pro[self.comboproducto.current ()],
                                                "id_bod": self.id_bode,"cantidad": self.entry_cantidad.get ()} )
                
                
                self.insert_datos.place_forget ()
                self.padre.llenar_treeview_detalle ()
            else:
                messagebox.showinfo ( self.root, message="No se permite un precio o producto bajo o igual a 0" )

        else:
            messagebox.showinfo ( self.root, message="No se permite un precio o producto bajo o igual a 0" )



