import tkinter as tk
from tkinter import ttk

class empleado:
    #Configuración de la ventana principal
    def __init__(self, root, db):

        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry('1100x400')
        self.root.title("Empleados")
        self.root.resizable(width=0, height=0)
        self.root.transient(root)
        self.__config_treeview_empleados()
        self.__config_buttons_empleado()

        self.root.mainloop()

    #Configuración de las tablas y su tamaño
    def __config_treeview_empleados(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4", "#5"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Apellido")
        self.treeview.heading("#3", text = "Telefono")
        self.treeview.heading("#4", text = "Sucursal")
        self.treeview.heading("#5", text = "Perfil")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#2", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#4", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#5", minwidth = 200, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 1100)
        self.llenar_treeview_empleado ()
        self.root.after ( 0, self.llenar_treeview_empleado )

    #Configuración de los botones
    def __config_buttons_empleado(self):
        ttk.Button(self.root, command = self.__Agregar_E, text="Agregar").place(x = 0, y = 350, width = 300, height = 50)
        ttk.Button(self.root, command = self.__Editar_E, text="Editar").place(x = 300, y = 350, width = 300, height = 50)
        ttk.Button(self.root, command = self.__Eliminar_E, text="Eliminar").place(x = 600, y = 350, width = 300, height = 50)

    def llenar_treeview_empleado(self):
        sql = """select id_empleado, nombre_emp, apellido_emp, telefono_emp, sucursal.nombre_suc, perfil.tipo_perfil
            from empleado join sucursal on empleado.sucursal_id_sucursal = sucursal.id_sucursal
            join perfil on empleado.perfil_id_perfil = perfil.id_perfil order by id_empleado asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4]), iid=i[0] )
            self.data = data

    def __Agregar_E(self):
        Add_Empleado(self.db, self)

    def __Editar_E(self):
        if (self.treeview.focus () != ""):
            sql = """select id_empleado, nombre_emp, apellido_emp, telefono_emp, sucursal.nombre_suc from empleado
                join sucursal on empleado.sucursal_id_sucursal = sucursal.id_sucursal
                join perfil on empleado.perfil_id_perfil = perfil.id_perfil where id_empleado = %(id_empleado)s"""
            row_data = self.db.run_select_filter ( sql, {"id_empleado": self.treeview.focus ()} )[0]
            editar_empleado ( self.db, self, row_data )

    def __Eliminar_E(self):
        sql = "select * from empleado where id_empleado = %(id_empleado)s"
        row_data = self.db.run_select_filter ( sql, {"id_sucursal": self.treeview.focus ()} )[0]
        Eliminar_Sucursal( self.db, self, row_data )

class Add_Empleado:
    #Configuración de la ventana agregar
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        self.add = tk.Toplevel()
        self.add.geometry('210x175')
        self.add.title("Agregar")
        self.add.resizable(width=0, height=0)
        #Contenido Ventana
        self.__config_labels()
        self.__config_entry()
        self.__config_buttons()

    #Configuración de los labels
    def __config_labels(self):
        tk.Label(self.add ,text = "Nombre: ").place(x = 0, y = 10, width = 100, height = 20)
        tk.Label(self.add ,text = "Apellido: ").place(x = 0, y = 35, width = 100, height = 20)
        tk.Label(self.add ,text = "Telefono: ").place(x = 0, y = 60, width = 100, height = 20)
        tk.Label(self.add ,text = "Sucursal: ").place(x = 0, y = 85, width = 100, height = 20)
        tk.Label(self.add ,text = "Perfil: ").place(x = 0, y = 110, width = 100, height = 20)


    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.add)
        self.entry_nombre.place(x = 100, y = 10, width = 100, height = 20)
        self.entry_apellido = ttk.Entry(self.add)
        self.entry_apellido.place(x = 100, y = 35, width = 100, height = 20)
        self.entry_telefono = ttk.Entry(self.add)
        self.entry_telefono.place(x = 100, y = 60, width = 100, height = 20)
        self.combosucursal = ttk.Combobox(self.add)
        self.combosucursal.place(x = 100, y = 85, width = 100, height = 20)
        self.combosucursal["values"], self.ids = self.__fill_combo_sucursal ()
        self.comboperfil = ttk.Combobox(self.add)
        self.comboperfil.place(x = 100, y = 110, width = 100, height = 20)
        self.comboperfil["values"], self.ids = self.__fill_combo_perfil ()

    #Configuración de los botones
    def __config_buttons(self):
        ttk.Button(self.add, command = self.__insertar, text="Aceptar").place(x = 70, y = 135, width = 90, height = 30)

    def __fill_combo_sucursal(self):
        sql = "select id_sucursal, nombre_suc from sucursal"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_perfil(self):
        sql = "select id_perfil, tipo_perfil from perfil"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert empleado (nombre_emp, apellido_emp, telefono_emp, sucursal_id_sucursal, perfil_id_perfil)
                values (%(nombre_emp)s, %(apellido_emp)s, %(telefono_emp)s, %(sucursal_id_sucursal)s, %(perfil_id_perfil)s);"""
        self.db.run_sql ( sql, {"nombre_emp": self.entry_nombre.get (),
                                "apellido_emp": self.entry_apellido.get (),
                                "telefono_emp": self.entry_telefono.get (),
                                "sucursal_id_sucursal": self.ids[self.combosucursal.current()],
                                "perfil_id_perfil": self.ids[self.comboperfil.current ()]} )


class editar_empleado:  # Clase para modificar
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
        self.insert_datos.geometry ( '250x290' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )


    def __config_label(self):
        tk.Label ( self.insert_datos, text= "Modificar " + (self.row_data[1]) ).place ( x=0, y=10, width=240, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=0, y=40, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Apellido: " ).place ( x=0, y=70, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Telefono: " ).place ( x=0, y=100, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Sucursal: " ).place ( x=0, y=130, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Perfil: " ).place ( x=0, y=160, width=100, height=20 )
        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = tk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 100, y = 40, width = 120, height = 20)
        self.entry_apellido = tk.Entry(self.insert_datos)
        self.entry_apellido.place(x = 100, y = 70, width = 120, height = 20)
        self.entry_telefono = tk.Entry(self.insert_datos)
        self.entry_telefono.place(x = 100, y = 100, width = 120, height = 20)
        self.combosuc = ttk.Combobox(self.insert_datos)
        self.combosuc.place(x = 100, y = 130, width = 120, height = 20)
        self.combosuc["values"], self.ids = self.fill_combosuc ()
        self.comboper = ttk.Combobox(self.insert_datos)
        self.comboper.place(x = 100, y = 160, width = 120, height = 20)
        self.comboper["values"], self.ids = self.fill_comboper ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_apellido.insert ( 0, self.row_data[2] )
        self.entry_telefono.insert ( 0, self.row_data[3] )
        self.combosuc.insert ( 0, self.row_data[4] )
        self.comboper.insert ( 0, self.row_data[5] )

        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=55, y=190, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update empleado set nombre_emp = %(nombre_emp)s, apellido_emp = %(apellido_emp)s,
            telefono_emp = %(telefono_emp)s, sucursal_id_sucursal = %(id_sucursal)s, %(id_perfil)
            where id_empleado = %(id_empleado)s"""
        self.db.run_sql ( sql, {"nombre_emp": self.entry_nombre.get (),
                                "apellido_emp": self.entry_apellido.get (),
                                "telefono_emp": self.entry_telefono.get (),
                                "id_sucursal": self.ids[self.combosuc.current ()],
                                "id_perfil": self.ids[self.comboper.current ()],
                                "id_empleado": self.row_data[0]} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_empleado ()

    def fill_combosuc(self):  #
        sql = "select id_sucursal, nombre_suc from sucursal"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def fill_comboper(self):  #
        sql = "select id_perfil, tipo_perfil from perfil"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

# Clase para eliminar
class Eliminar_Empleado:
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
        tk.Label ( self.del_datos, text= "Apellido: " + (self.row_data[1])).place( x=5, y=30, width=250, height=20 )
        # tk.Label ( self.del_datos, text= "Sucursal: " + (self.row_data[1])).place( x=5, y=30, width=250, height=20 ) # el id es int

    def __config_button(self):
        ttk.Button(self.del_datos, command = self.__Cancelar, text="Cancelar").place(x = 0, y = 80, width = 100, height = 50)
        ttk.Button(self.del_datos, command = self.__Aceptar, text="Aceptar").place(x = 150, y = 80, width = 100, height = 50)

    def __Cancelar(self):
        self.del_datos.destroy()

    def __Aceptar(self):
        sql = "delete from empleado where id_empleado = %(id_empleado)s"
        self.db.run_sql ( sql, {"id_empleado": int ( self.row_data[0] )} )
        self.del_datos.destroy ()
        self.padre.llenar_treeview_perfil ()
