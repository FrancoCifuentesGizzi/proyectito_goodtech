import tkinter as tk
from tkinter import ttk
from detalle import detalle

class venta:
    #Configuración de la ventana principal
    def __init__(self, root, db):

        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry('1100x400')
        self.root.title("Ventas")
        self.root.resizable(width=0, height=0)
        self.root.transient(root)
        self.__config_treeview_venta()
        self.__config_buttons_venta()

        self.root.mainloop()

    #Configuración de las tablas y su tamaño
    def __config_treeview_venta(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4", "#5"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Fecha")
        self.treeview.heading("#2", text = "Total")
        self.treeview.heading("#3", text = "Sucursal")
        self.treeview.heading("#4", text = "Empleado")
        self.treeview.heading("#5", text = "Cliente")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#2", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#4", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#5", minwidth = 200, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 1100)
        self.llenar_treeview_venta ()
        self.root.after ( 0, self.llenar_treeview_venta )

    #Configuración de los botones
    def __config_buttons_venta(self):
        ttk.Button(self.root, command = self.__Agregar_V, text="Agregar Venta").place(x = 0, y = 350, width = 275, height = 50)
        ttk.Button(self.root, command = self.__Editar_V, text="Modificar Venta").place(x = 275, y = 350, width = 275, height = 50)
        ttk.Button(self.root, command = self.__Editar_D, text="Ver Detalles").place(x = 550, y = 350, width = 275, height = 50)
        ttk.Button(self.root, command = self.__Eliminar_V, text="Eliminar Venta").place(x = 825, y = 350, width = 275, height = 50)

    def llenar_treeview_venta(self):
        sql = """select id_venta, fecha, total, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli from venta
            join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
            join empleado on venta.empleado_id_empleado = empleado.id_empleado
            join cliente on venta.cliente_id_cliente = cliente.id_cliente order by id_venta asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5]), iid=i[0] )
            self.data = data


    def __Agregar_V(self):
        Add_Venta(self.db, self)

    def __Editar_V(self):
        if (self.treeview.focus () != ""):
            sql = """select id_venta, fecha, total, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli from venta
                join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
                join empleado on venta.empleado_id_empleado = empleado.id_empleado
                join cliente on venta.cliente_id_cliente = cliente.id_cliente where id_venta = %(id_venta)s"""
            row_data = self.db.run_select_filter ( sql, {"id_venta": self.treeview.focus ()} )[0]
            editar_venta ( self.db, self, row_data )

    def __Editar_D(self):
        if (self.treeview.focus () != ""):
            sql = """select id_venta, fecha, total, sucursal.nombre_suc, empleado.nombre_emp, cliente.nombre_cli from venta
                join sucursal on venta.sucursal_id_sucursal = sucursal.id_sucursal
                join empleado on venta.empleado_id_empleado = empleado.id_empleado
                join cliente on venta.cliente_id_cliente = cliente.id_cliente where id_venta = %(id_venta)s"""
            row_data = self.db.run_select_filter ( sql, {"id_venta": self.treeview.focus ()} )[0]
            detalle ( self.db, self, row_data )

    def __Eliminar_V(self):
        sql = "select * from venta where id_venta = %(id_venta)s"
        row_data = self.db.run_select_filter ( sql, {"id_venta": self.treeview.focus ()} )[0]
        Eliminar_Venta( self.db, self, row_data )

class Add_Venta:
    #Configuración de la ventana agregar
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

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
        tk.Label(self.add ,text = "Fecha: ").place(x = 0, y = 10, width = 100, height = 20)
        tk.Label(self.add ,text = "Sucursal: ").place(x = 0, y = 35, width = 100, height = 20)
        tk.Label(self.add ,text = "Empleado: ").place(x = 0, y = 60, width = 100, height = 20)
        tk.Label(self.add ,text = "Cliente: ").place(x = 0, y = 85, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_fecha = ttk.Entry(self.add)
        self.entry_fecha.place(x = 100, y = 10, width = 100, height = 20)
        self.combosucursal = ttk.Combobox(self.add)
        self.combosucursal.place(x = 100, y = 35, width = 100, height = 20)
        self.combosucursal["values"], self.suc = self.__fill_combo_suc ()
        self.comboempleado = ttk.Combobox(self.add)
        self.comboempleado.place(x = 100, y = 60, width = 100, height = 20)
        self.comboempleado["values"], self.wrk = self.__fill_combo_wrk ()
        self.combocliente = ttk.Combobox(self.add)
        self.combocliente.place(x = 100, y = 85, width = 100, height = 20)
        self.combocliente["values"], self.client = self.__fill_combo_client ()

        #Configuración de los botones
    def __config_buttons(self):
        ttk.Button(self.add, text="Aceptar",
                  command = self.__insertar).place(x = 55, y = 120, width = 105, height = 30)

    def __fill_combo_suc(self):
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_wrk(self):
        sql = "select id_empleado, nombre_emp from empleado order by id_empleado asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_client(self):
        sql = "select id_cliente, nombre_cli from cliente order by id_cliente asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert venta (fecha, total, sucursal_id_sucursal, empleado_id_empleado, cliente_id_cliente )
            values (%(fecha)s, %(total)s, %(sucursal_id_sucursal)s, %(empleado_id_empleado)s, %(cliente_id_cliente)s);"""
        self.db.run_sql ( sql, {"fecha": self.entry_fecha.get (),
                                "total": 0,
                                "sucursal_id_sucursal": self.suc[self.combosucursal.current ()],
                                "empleado_id_empleado": self.wrk[self.comboempleado.current ()],
                                "cliente_id_cliente": self.client[self.combocliente.current ()]} )
        self.add.destroy ()
        self.padre.llenar_treeview_venta ()


class editar_venta:  # Clase para modificar
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.insert_datos = tk.Toplevel ()
        self.__config_window ()
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_window(self):  # Configuración de la ventana.
        self.insert_datos.geometry ( '210x200' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )

    def __config_label(self):
        tk.Label ( self.insert_datos, text= "Modificando Venta").place ( x=0, y=10, width=240, height=20 )
        tk.Label ( self.insert_datos, text="Fecha: " ).place ( x=0, y=35, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Sucursal: " ).place ( x=0, y=60, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Empleado: " ).place ( x=0, y=85, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Cliente: " ).place ( x=0, y=110, width=100, height=20 )

# Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_fecha = ttk.Entry(self.insert_datos)
        self.entry_fecha.place(x = 100, y = 35, width = 100, height = 20)
        self.combosucursal = ttk.Combobox(self.insert_datos)
        self.combosucursal.place(x = 100, y = 60, width = 100, height = 20)
        self.combosucursal["values"], self.suc = self.fill_combo_suc ()
        self.comboempleado = ttk.Combobox ( self.insert_datos )
        self.comboempleado.place ( x=100, y=85, width=100, height=20 )
        self.comboempleado["values"], self.wrk = self.fill_combo_wrk ()
        self.combocliente = ttk.Combobox ( self.insert_datos )
        self.combocliente.place ( x=100, y=110, width=100, height=20 )
        self.combocliente["values"], self.client = self.fill_combo_client ()
        self.entry_fecha.insert ( 0, self.row_data[1] )
        self.combosucursal.insert ( 0, self.row_data[3] )
        self.comboempleado.insert ( 0, self.row_data[4] )
        self.combocliente.insert ( 0, self.row_data[5] )
        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=55, y=160, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update venta set fecha = %(fecha)s, sucursal_id_sucursal = %(id_sucursal)s,
                empleado_id_empleado = %(id_empleado)s, cliente_id_cliente = %(id_cliente)s
                where id_venta = %(id_venta)s"""
        self.db.run_sql ( sql, {"fecha": self.entry_fecha.get (),
                                "id_sucursal": self.suc[self.combosucursal.current ()],
                                "id_empleado": self.wrk[self.comboempleado.current ()],
                                "id_cliente": self.client[self.combocliente.current ()],
                                "id_venta": self.row_data[0]} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_venta ()

    def fill_combo_suc(self):  #
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def fill_combo_wrk(self):  #
        sql = "select id_empleado, nombre_emp from empleado order by id_empleado asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def fill_combo_client(self):  #
        sql = "select id_cliente, nombre_cli from cliente order by id_cliente asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]


class Eliminar_Venta:
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
        self.del_datos.geometry ( '250x170' )
        self.del_datos.title ( "Eliminando datos" )
        self.del_datos.resizable ( width=0, height=0 )

    def __config_label(self):
        tk.Label ( self.del_datos, text= "Se eliminará la venta: ").place ( x=5, y=10, width=250, height=20 )

    def __config_button(self):
        ttk.Button(self.del_datos, command = self.__Cancelar, text="Cancelar").place(x = 0, y = 120, width = 100, height = 50)
        ttk.Button(self.del_datos, command = self.__Aceptar, text="Aceptar").place(x = 150, y = 120, width = 100, height = 50)

    def __Cancelar(self):
        self.del_datos.destroy()

    def __Aceptar(self):
        sql = "delete from venta where id_venta = %(id_venta)s"
        self.db.run_sql ( sql, {"id_venta": int ( self.row_data[0] )} )
        self.del_datos.destroy ()
        self.padre.llenar_treeview_venta ()
