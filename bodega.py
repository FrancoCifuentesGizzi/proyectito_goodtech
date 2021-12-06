import tkinter as tk
from tkinter import ttk

class bodega:
    #Configuración de la ventana principal
    def __init__(self, root, db):

        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry('900x400')
        self.root.title("Bodegas")
        self.root.resizable(width=0, height=0)
        self.root.transient(root)

        self.__config_treeview_bodega()
        self.__config_buttons_bodega()

        self.root.mainloop()

    #Configuración de las tablas y su tamaño
    def __config_treeview_bodega(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3", "#4"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Direccion")
        self.treeview.heading("#3", text = "Telefono")
        self.treeview.heading("#4", text = "Ciudad")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#2", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#4", minwidth = 200, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 1100)
        self.llenar_treeview_bodega ()
        self.root.after ( 0, self.llenar_treeview_bodega)

    #Configuración de los botones
    def __config_buttons_bodega(self):
        tk.Button(self.root, text="Agregar bodega",
            command = self.__Agregar_B).place(x = 0, y = 350, width = 300, height = 50)
        tk.Button(self.root, command = self.__Editar_S, text="Modificar datos").place(x = 300, y = 350, width = 300, height = 50)
        tk.Button(self.root, command = self.__Eliminar_S, text="Eliminar bodega").place(x = 600, y = 350, width = 300, height = 50)

    def llenar_treeview_bodega(self):
        sql = """select id_bodega, nombre_bod, direccion_bod, telefono_bod, nombre_ciu
           from bodega join ciudad on bodega.ciudad_id_ciudad = ciudad.id_ciudad"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1], i[2], i[3], i[4]), iid=i[0])
            self.data = data

    def __Agregar_B(self):
        Add_bodega(self.db, self)

    def __Editar_S(self):
        if (self.treeview.focus () != ""):
            sql = "select id_bodega, nombre_bod, direccion_bod, telefono_bod, ciudad.nombre_ciu from bodega " \
                  "join ciudad on bodega.ciudad_id_ciudad = ciudad.id_ciudad where id_bodega = %(id_bodega)s"
            row_data = self.db.run_select_filter ( sql, {"id_bodega": self.treeview.focus ()} )[0]
            editar_bodega ( self.db, self, row_data )

    def __Eliminar_S():
        print("Heyo")
        #Del_Empleado

class Add_bodega:
    #Configuración de la ventana agregar
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        self.add = tk.Toplevel()
        self.add.geometry('210x170')
        self.add.title("Agregar")
        self.add.resizable(width=0, height=0)
        #Contenido Ventana
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    #Configuración de los labels
    def __config_label(self):
        tk.Label(self.add ,text = "Nombre: ").place(x = 0, y = 10, width = 100, height = 20)
        tk.Label(self.add ,text = "Direccion: ").place(x = 0, y = 30, width = 100, height = 20)
        tk.Label(self.add ,text = "Telefono: ").place(x = 0, y = 50, width = 100, height = 20)
        tk.Label(self.add ,text = "Ciudad: ").place(x = 0, y = 70, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = tk.Entry(self.add)
        self.entry_nombre.place(x = 100, y = 10, width = 100, height = 20)
        self.entry_direccion = tk.Entry(self.add)
        self.entry_direccion.place(x = 100, y = 30, width = 100, height = 20)
        self.entry_telefono = tk.Entry(self.add)
        self.entry_telefono.place(x = 100, y = 50, width = 100, height = 20)
        self.combo_ciudad = ttk.Combobox(self.add)
        self.combo_ciudad.place(x = 100, y = 70, width = 100, height = 20)
        self.combo_ciudad["values"], self.ids = self.__fill_combo ()

        #Configuración de los botones
    def __config_button(self):
        tk.Button(self.add, text="Aceptar", command = self.__insertar).place(x = 55, y = 120, width = 105, height = 30)

    def __fill_combo(self):
        sql = "select id_ciudad, nombre_ciu from ciudad"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into bodega (nombre_bod, direccion_bod, telefono_bod, ciudad_id_ciudad )
            values (%(nombre_bod)s, %(direccion_bod)s, %(telefono_bod)s, %(ciudad_id_ciudad)s)"""
        self.db.run_sql ( sql, {"nombre_bod": self.entry_nombre.get (),
                                "direccion_bod": self.entry_direccion.get (),
                                "telefono_bod": self.entry_telefono.get (),
                                "ciudad_id_ciudad": self.ids[self.combo_ciudad.current ()]} )
        self.add.destroy ()
        self.padre.llenar_treeview_bodega()


class editar_bodega:  # Clase para modificar
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
        self.insert_datos.geometry ( '250x260' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )


    def __config_label(self):
        tk.Label ( self.insert_datos, text= "Modificar " + (self.row_data[1]) ).place ( x=5, y=10, width=250, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=0, y=30, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Direccion: " ).place ( x=0, y=60, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Telefono: " ).place ( x=0, y=90, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Ciudad: " ).place ( x=0, y=120, width=100, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = tk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 100, y = 30, width = 100, height = 20)
        self.entry_direccion = tk.Entry(self.insert_datos)
        self.entry_direccion.place(x = 100, y = 60, width = 100, height = 20)
        self.entry_telefono = tk.Entry(self.insert_datos)
        self.entry_telefono.place(x = 100, y = 90, width = 100, height = 20)
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 100, y = 120, width = 100, height = 20)
        self.combo["values"], self.ids = self.fill_combo ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_direccion.insert ( 0, self.row_data[2] )
        self.entry_telefono.insert ( 0, self.row_data[3] )
        self.combo.insert ( 0, self.row_data[4] )

        # Configuración de los botones

    def __config_button(self):
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=55, y=160, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update bodega set nombre_bod = %(nombre_bod)s, direccion_bod = %(direccion_bod)s,
                telefono_bod = %(telefono_bod)s, ciudad_id_ciudad = %(id_ciudad)s
                where id_bodega = %(id_bodega)s"""
        self.db.run_sql ( sql, {"nombre_bod": self.entry_nombre.get (),
                                "direccion_bod": self.entry_direccion.get (),
                                "telefono_bod": self.entry_telefono.get (),
                                "id_ciudad": self.ids[self.combo.current ()],
                                "id_bodega": self.row_data[0]} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_bodega ()

    def fill_combo(self):  #
        sql = "select id_ciudad, nombre_ciu from ciudad"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]
