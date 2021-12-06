import tkinter as tk
from tkinter import ttk



class jugador:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel ()
        self.root.geometry ( '600x400' )
        self.root.title ( "Equipos" )
        self.root.resizable ( width=0, height=0 )

        # toplevel modal
        self.root.transient ( root )

        #
        self.__config_treeview_jugador ()
        self.__config_buttons_jugador ()

    def __config_treeview_jugador(self):
        self.treeview = ttk.Treeview ( self.root )
        self.treeview.configure ( columns=("#1", "#2") )
        self.treeview.heading ( "#0", text="Id" )
        self.treeview.heading ( "#1", text="Jugador" )
        self.treeview.heading ( "#2", text="Equipo" )
        self.treeview.column ( "#0", minwidth=100, width=100, stretch=False )
        self.treeview.column ( "#1", minwidth=300, width=300, stretch=False )
        self.treeview.column ( "#2", minwidth=300, width=300, stretch=False )
        self.treeview.place ( x=0, y=0, height=350, width=700 )
        self.llenar_treeview_jugador ()
        self.root.after ( 0, self.llenar_treeview_jugador )

    def __config_buttons_jugador(self):
        tk.Button ( self.root, text="Insertar jugador",
                    command=self.__insertar_jugador ).place ( x=0, y=350, width=200, height=50 )
        tk.Button ( self.root, text="Modificar jugador",
                    command=self.__modificar_jugador ).place ( x=200, y=350, width=200, height=50 )
        tk.Button ( self.root, text="Eliminar jugador",
                    command=self.__eliminar_jugador ).place ( x=400, y=350, width=200, height=50 )
        tk.Button ( self.root, text="Ver equipos",
                    command=self.__ver_equipos ).place ( x=600, y=350, width=100, height=50 )

    def llenar_treeview_jugador(self):
        sql = """select id_jugador, nom_jugador, ape_jugador, nom_equipo 
        from jugador join equipo on jugador.id_equipo = equipo.id_equipo;"""
        data = self.db.run_select ( sql )

        if (data != self.data):
            self.treeview.delete ( *self.treeview.get_children () )  # Elimina todos los rows del treeview
            for i in data:
                self.treeview.insert ( "", "end", text=i[0],
                                       values=(i[1] + " " + i[2], i[3]), iid=i[0], tags="rojo" )
            self.data = data

    def __insertar_jugador(self):
        insertar_jugador ( self.db, self )

    def __modificar_jugador(self):
        if (self.treeview.focus () != ""):
            sql = """select id_jugador, nom_jugador, ape_jugador, equipo.nom_equipo 
            from jugador join equipo on jugador.id_equipo = equipo.id_equipo 
            where id_jugador = %(id_jugador)s"""

            row_data = self.db.run_select_filter ( sql, {"id_jugador": self.treeview.focus ()} )[0]
            modificar_jugador ( self.db, self, row_data )

    def __eliminar_jugador(self):
        sql = "delete from jugador where id_jugador = %(id_jugador)s"
        self.db.run_sql ( sql, {"id_jugador": self.treeview.focus ()} )
        self.llenar_treeview_jugador ()

    def __ver_equipos(self):
        equipo ( self.db )


class insertar_jugador:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db
        self.insert_datos = tk.Toplevel ()
        self.__config_window ()
        self.__config_label ()
        self.__config_entry ()
        self.__config_button ()

    def __config_window(self):
        self.insert_datos.geometry ( '200x120' )
        self.insert_datos.title ( "Insertar jugador" )
        self.insert_datos.resizable ( width=0, height=0 )

    def __config_label(self):
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=10, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=40, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Equipo: " ).place ( x=10, y=70, width=80, height=20 )

    def __config_entry(self):
        self.entry_nombre = tk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=110, y=10, width=80, height=20 )
        self.entry_apellido = tk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=110, y=40, width=80, height=20 )
        self.combo = ttk.Combobox ( self.insert_datos )
        self.combo.place ( x=110, y=70, width=80, height=20 )
        self.combo["values"], self.ids = self.__fill_combo ()

    def __config_button(self):
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.__insertar ).place ( x=0, y=100, width=200, height=20 )

    def __fill_combo(self):
        sql = "select id_equipo, nom_equipo from equipo"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __insertar(self):  # Insercion en la base de datos.
        sql = """insert jugador (id_equipo, nom_jugador, ape_jugador) 
            values (%(id_equipo)s, %(nom_jugador)s, %(ape_jugador)s)"""
        self.db.run_sql ( sql, {"id_equipo": self.ids[self.combo.current ()],
                                "nom_jugador": self.entry_nombre.get (), "ape_jugador": self.entry_apellido.get ()} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_jugador ()


class modificar_jugador:
    def __init__(self, db, padre, row_data):
        self.padre = padre
        self.db = db
        self.row_data = row_data
        self.insert_datos = tk.Toplevel ()
        self.config_window ()
        self.config_label ()
        self.config_entry ()
        self.config_button ()

    def config_window(self):  # Settings
        self.insert_datos.geometry ( '200x120' )
        self.insert_datos.title ( "Modificar jugador" )
        self.insert_datos.resizable ( width=0, height=0 )

    def config_label(self):  # Labels
        tk.Label ( self.insert_datos, text="Nombre: " ).place ( x=10, y=10, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Apellido: " ).place ( x=10, y=40, width=80, height=20 )
        tk.Label ( self.insert_datos, text="Equipo: " ).place ( x=10, y=70, width=80, height=20 )

    def config_entry(self):  # Se configuran los inputs
        self.entry_nombre = tk.Entry ( self.insert_datos )
        self.entry_nombre.place ( x=110, y=10, width=80, height=20 )
        self.entry_apellido = tk.Entry ( self.insert_datos )
        self.entry_apellido.place ( x=110, y=40, width=80, height=20 )
        self.combo = ttk.Combobox ( self.insert_datos )
        self.combo.place ( x=110, y=70, width=80, height=20 )
        self.combo["values"], self.ids = self.fill_combo ()
        self.entry_nombre.insert ( 0, self.row_data[1] )
        self.entry_apellido.insert ( 0, self.row_data[2] )
        self.combo.insert ( 0, self.row_data[3] )

    def config_button(self):  # Botón aceptar, llama a la función modificar cuando es clickeado.
        tk.Button ( self.insert_datos, text="Aceptar",
                    command=self.modificar ).place ( x=0, y=100, width=200, height=20 )

    def modificar(self):  # Insercion en la base de datos.
        sql = """update jugador set nom_jugador = %(nom_jugador)s, ape_jugador = %(ape_jugador)s, 
            id_equipo = %(id_equipo)s where id_jugador = %(id_jugador)s"""
        self.db.run_sql ( sql, {"nom_jugador": self.entry_nombre.get (),
                                "ape_jugador": self.entry_apellido.get (), "id_equipo": self.ids[self.combo.current ()],
                                "id_jugador": int ( self.row_data[0] )} )
        self.insert_datos.destroy ()
        self.padre.llenar_treeview_jugador ()

    def fill_combo(self):  #
        sql = "select id_equipo, nom_equipo from equipo"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]
