import tkinter as tk
from tkinter import ttk

class producto:
    #Configuración de la ventana principal
    def __init__(self, root, db):

        self.db = db
        self.data = []

        self.root = tk.Toplevel()
        self.root.geometry('700x400')
        self.root.title("Productos")
        self.root.resizable(width=0, height=0)
        self.root.transient(root)

        self.__config_treeview_producto()
        self.__config_buttons_producto()

        self.root.mainloop()

    #Configuración de las tablas y su tamaño
    def __config_treeview_producto(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1", "#2", "#3"))
        self.treeview.heading("#0", text = "Id")
        self.treeview.heading("#1", text = "Nombre")
        self.treeview.heading("#2", text = "Precio")
        self.treeview.heading("#3", text = "Marca")
        self.treeview.column("#0", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#2", minwidth = 200, width = 200, stretch = False)
        self.treeview.column("#3", minwidth = 200, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        self.llenar_treeview_producto ()
        self.root.after ( 0, self.llenar_treeview_producto)

    #Configuración de los botones
    def __config_buttons_producto(self):
        ttk.Button(self.root, command = self.__Agregar_P, text="Agregar producto").place(x = 0, y = 350, width = 233, height = 50)
        ttk.Button(self.root, command = self.__Editar_P, text="Modificar datos").place(x = 233, y = 350, width = 233, height = 50)
        ttk.Button(self.root, command = self.__Eliminar_P, text="Eliminar producto").place(x = 466, y = 350, width = 233, height = 50)

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
        Add_producto(self.db, self)

    def __Editar_P(self):
        if (self.treeview.focus () != ""):
            sql = """select id_producto, nombre_pro, precio_pro, marca.nombre_marca, bodega.nombre_bod from producto
                join marca on producto.marca_id_marca = marca.id_marca where id_producto = %(id_producto)s"""
            row_data = self.db.run_select_filter ( sql, {"id_producto": self.treeview.focus ()} )[0]
            editar_producto ( self.db, self, row_data )

    def __Eliminar_P(self):
        sql = "select * from producto where id_producto = %(id_producto)s"
        row_data = self.db.run_select_filter ( sql, {"id_producto": self.treeview.focus ()} )[0]
        Eliminar_Producto( self.db, self, row_data )

class Add_producto:
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
        tk.Label(self.add ,text = "Precio: ").place(x = 0, y = 35, width = 100, height = 20)
        tk.Label(self.add ,text = "Marca: ").place(x = 0, y = 60, width = 100, height = 20)

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.add)
        self.entry_nombre.place(x = 100, y = 10, width = 100, height = 20)
        self.entry_precio = ttk.Entry(self.add)
        self.entry_precio.place(x = 100, y = 35, width = 100, height = 20)
        self.combo_marca = ttk.Combobox(self.add)
        self.combo_marca.place(x = 100, y = 60, width = 100, height = 20)
        self.combo_marca["values"], self.marca = self.__fill_combo_marca ()

        #Configuración de los botones
    def __config_button(self):
        ttk.Button(self.add, text="Aceptar", command = self.__insertar).place(x = 55, y = 130, width = 105, height = 25)

    def __fill_combo_marca(self):
        sql = "select id_marca, nombre_marca from marca"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert into producto (nombre_pro, precio_pro, marca_id_marca )
            values (%(nombre_pro)s, %(precio_pro)s, %(marca_id_marca)s)"""
        self.db.run_sql ( sql, {"nombre_pro": self.entry_nombre.get (),
                                "precio_pro": self.entry_precio.get (),
                                "marca_id_marca": self.marca[self.combo_marca.current ()]} )
        self.add.destroy ()
        self.padre.llenar_treeview_producto()


class editar_producto:  # Clase para modificar
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
        self.insert_datos.geometry ( '220x190' )
        self.insert_datos.title ( "Editar datos" )
        self.insert_datos.resizable ( width=0, height=0 )


    def __config_label(self):
        tk.Label ( self.insert_datos, text= "Modificar " + (self.row_data[1]) ).place ( x=0, y=10, width=240, height=20 )
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=0, y=35, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Precio: " ).place ( x=0, y=60, width=100, height=20 )
        tk.Label ( self.insert_datos, text="Marca: " ).place ( x=0, y=85, width=100, height=20 )

        # Configuración de las casillas que el usuario ingresa info

    def __config_entry(self):
        self.entry_nombre = ttk.Entry(self.insert_datos)
        self.entry_nombre.place(x = 100, y = 35, width = 100, height = 20)
        self.entry_precio = ttk.Entry(self.insert_datos)
        self.entry_precio.place(x = 100, y = 60, width = 100, height = 20)
        self.combo_marca = ttk.Combobox(self.insert_datos)
        self.combo_marca.place(x = 100, y = 85, width = 100, height = 20)
        self.combo_marca["values"], self.marca = self.__fill_combo_marca ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_precio.insert ( 0, self.row_data[2] )
        self.combo_marca.insert ( 0, self.row_data[3] )

        # Configuración de los botones

    def __config_button(self):
        ttk.Button ( self.insert_datos, command=self.modificar, text="Aceptar" ).place ( x=64, y=150, width=105, height=25 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update producto set nombre_pro = %(nombre_pro)s, precio_pro = %(precio_pro)s,
            marca_id_marca = %(id_marca)s, where id_producto = %(id_producto)s"""
        self.db.run_sql ( sql, {"nombre_pro": self.entry_nombre.get (),
                                "precio_pro": self.entry_precio.get (),
                                "id_marca": self.marca[self.combo_marca.current ()],
                                "id_producto": self.row_data[0]} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_producto ()

    def __fill_combo_marca(self):
        sql = "select id_marca, nombre_marca from marca"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

class Eliminar_Producto:
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
        self.del_datos.geometry ( '250x150' )
        self.del_datos.title ( "Eliminando datos" )
        self.del_datos.resizable ( width=0, height=0 )

    def __config_label(self):
        tk.Label ( self.del_datos, text= "Se eliminará el siguiente dato: ").place( x=5, y=10, width=250, height=20 )
        tk.Label ( self.del_datos, text= "Nombre: " + (self.row_data[1])).place( x=5, y=30, width=250, height=20 )
        # tk.Label ( self.del_datos, text= "Marca: " + (self.row_data[3])).place( x=5, y=50, width=250, height=20 ) # el row_data[3] es solo la id de la marca

    def __config_button(self):
        ttk.Button(self.del_datos, command = self.__Cancelar, text="Cancelar").place(x = 0, y = 100, width = 100, height = 50)
        ttk.Button(self.del_datos, command = self.__Aceptar, text="Aceptar").place(x = 150, y = 100, width = 100, height = 50)

    def __Cancelar(self):
        self.del_datos.destroy()

    def __Aceptar(self):
        sql = "delete from producto where id_producto = %(id_producto)s"
        self.db.run_sql ( sql, {"id_producto": int ( self.row_data[0] )} )
        self.del_datos.destroy ()
        self.padre.llenar_treeview_producto ()
