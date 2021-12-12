import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class empleado:
    #Configuración de la ventana principal
    def __init__(self, root, db, b5, __limpia_pantalla):
        self.db = db
        self.data = []
        self.root = root
        self.boton = b5
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_treeview_empleados()
        self.__config_buttons_empleado()

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
        self.treeview.column ( "#0", minwidth=30, width=60, stretch=False )
        self.treeview.column ( "#1", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#2", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#3", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#4", minwidth=50, width=135, stretch=False )
        self.treeview.column ( "#5", minwidth=50, width=135, stretch=False )
        self.treeview.place ( x=189, y=26, height=375, width=735 )
        self.llenar_treeview_empleado ()
        self.root.after ( 0, self.llenar_treeview_empleado )

    #Configuración de los botones
    def __config_buttons_empleado(self):
        ttk.Button ( self.treeview, text="Insertar Empleado",
                     command=self.__Agregar_E ).place ( x=0, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Modificar Empleado",
                     command=self.__Editar_E ).place ( x=183, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Eliminar Empleado",
                     command=self.__Eliminar_E ).place ( x=366, y=340, width=183, height=35 )
        ttk.Button ( self.treeview, text="Cerrar",
                     command=self.__Cerrar_E ).place ( x=549, y=340, width=183, height=35 )

    def llenar_treeview_empleado(self):
        sql = """select id_empleado, nombre_emp, apellido_emp, telefono_emp, sucursal.nombre_suc, perfil.tipo_perfil from empleado
            join sucursal on empleado.sucursal_id_sucursal = sucursal.id_sucursal
            join perfil on empleado.perfil_id_perfil = perfil.id_perfil
            order by id_empleado asc"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4], i[5]), iid=i[0] )
            self.data = data

    def __Agregar_E(self):
        Add_Empleado(self.db, self, self.root)

    def __Editar_E(self):
        if (self.treeview.focus () != ""):
            sql = """select id_empleado, nombre_emp, apellido_emp, telefono_emp, sucursal.nombre_suc, perfil.tipo_perfil from empleado
                join sucursal on empleado.sucursal_id_sucursal = sucursal.id_sucursal
                join perfil on empleado.perfil_id_perfil = perfil.id_perfil
                where id_empleado = %(id_empleado)s"""
            row_data = self.db.run_select_filter ( sql, {"id_empleado": self.treeview.focus ()} )[0]
            editar_empleado ( self.db, self, row_data, self.root )
        else:
            messagebox.showinfo ( self.root, message="Seleccione un objeto de la lista" )

    def __Eliminar_E(self):
        if (self.treeview.focus () != ""):
            ke_dijo = messagebox.askyesno ( message="¿Seguro que desea borrar esta información?" )
            if (ke_dijo == True):
                sql = "delete from empleado where id_empleado = %(id_empleado)s"
                self.db.run_sql ( sql, {"id_empleado": self.treeview.focus ()} )
                self.llenar_treeview_empleado ()

    def __Cerrar_E(self):
        self.boton.config ( background="dark goldenrod" )
        self.treeview.place_forget ()
        self.__limpia_pantalla ()

class Add_Empleado:
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
        Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Telefono: " ).place ( x=10, y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Sucursal: " ).place ( x=270, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Perfil: " ).place ( x=270, y=35, width=80, height=20 )

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=90, y=10, width=150, height=20 )
        self.entry_apellido = ttk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=90, y=35, width=150, height=20 )
        self.entry_telefono = ttk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=90, y=60, width=150, height=20 )
        self.combosucursal = ttk.Combobox ( self.insert_datos )
        self.combosucursal.place ( x=340, y=10, width=150, height=20 )
        self.combosucursal["values"], self.suc = self.__fill_combo_sucursal ()
        self.comboperfil = ttk.Combobox ( self.insert_datos )
        self.comboperfil.place ( x=340, y=35, width=150, height=20 )
        self.comboperfil["values"], self.per = self.__fill_combo_perfil ()

    #Configuración de los botones
    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                     command=self.__insertar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def __fill_combo_sucursal(self):
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __fill_combo_perfil(self):
        sql = "select id_perfil, tipo_perfil from perfil order by id_perfil asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert empleado (nombre_emp, apellido_emp, telefono_emp, sucursal_id_sucursal, perfil_id_perfil)
                values (%(nombre_emp)s, %(apellido_emp)s, %(telefono_emp)s, %(sucursal_id_sucursal)s, %(perfil_id_perfil)s);"""
        self.db.run_sql ( sql, {"nombre_emp": self.entry_nombre.get (),
                                "apellido_emp": self.entry_apellido.get (),
                                "telefono_emp": self.entry_telefono.get (),
                                "sucursal_id_sucursal": self.suc[self.combosucursal.current()],
                                "perfil_id_perfil": self.per[self.comboperfil.current()]})
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_empleado()

    def __borra(self):
        self.insert_datos.place_forget ()

class editar_empleado:  # Clase para modificar
    def __init__(self, db, padre, row_data, root):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.root = root
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def config_window(self):  # Configuración de la ventana.
        self.insert_datos.geometry ( '250x290' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )


    def __config_label(self):
        self.insert_datos = LabelFrame ( self.root, text="" )
        self.insert_datos.place ( x=189, y=405, width=735, height=120 )
        Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=35, width=80, height=20 )
        Label ( self.insert_datos, text="Telefono: " ).place ( x=10, y=60, width=80, height=20 )
        Label ( self.insert_datos, text="Sucursal: " ).place ( x=270, y=10, width=80, height=20 )
        Label ( self.insert_datos, text="Perfil: " ).place ( x=270, y=35, width=80, height=20 )

    def __config_entry(self):
        self.entry_nombre = ttk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=90, y=10, width=150, height=20 )
        self.entry_apellido = ttk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=90, y=35, width=150, height=20 )
        self.entry_telefono = ttk.Entry ( self.insert_datos )
        self.entry_telefono.place ( x=90, y=60, width=150, height=20 )
        self.combosucursal = ttk.Combobox ( self.insert_datos )
        self.combosucursal.place ( x=340, y=10, width=150, height=20 )
        self.combosucursal["values"], self.suc = self.__fill_combo_sucursal ()
        self.comboperfil = ttk.Combobox ( self.insert_datos )
        self.comboperfil.place ( x=340, y=35, width=150, height=20 )
        self.comboperfil["values"], self.per = self.__fill_combo_perfil ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_apellido.insert ( 0, self.row_data[2] )
        self.entry_telefono.insert ( 0, self.row_data[3] )
        self.combosucursal.insert ( 0, self.row_data[4] )
        self.comboperfil.insert ( 0, self.row_data[5] )

    def __config_button(self):
        ttk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=510, y=10, width=200, height=30 )
        ttk.Button ( self.insert_datos, text="Cancelar",
                     command=self.__borra ).place ( x=510, y=40, width=200, height=30 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update empleado set nombre_emp = %(nombre_emp)s, apellido_emp = %(apellido_emp)s,
                telefono_emp = %(telefono_emp)s, sucursal_id_sucursal = %(id_sucursal)s, perfil_id_perfil = %(id_perfil)s
                where id_empleado = %(id_empleado)s"""
        self.db.run_sql ( sql, {"nombre_emp": self.entry_nombre.get (),
                                "apellido_emp": self.entry_apellido.get (),
                                "telefono_emp": self.entry_telefono.get (),
                                "id_sucursal": self.suc[self.combosucursal.current ()],
                                "id_perfil": self.per[self.comboperfil.current ()],
                                "id_empleado": self.row_data[0]} )
        self.insert_datos.place_forget ()
        self.padre.llenar_treeview_empleado ()

    def __fill_combo_sucursal(self):  #
        sql = "select id_sucursal, nombre_suc from sucursal order by id_sucursal asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]
    
    def __fill_combo_perfil(self):  #
        sql = "select id_perfil, tipo_perfil from perfil order by id_perfil asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __borra(self):
        self.insert_datos.place_forget ()