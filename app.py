import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk
from tkinter import messagebox

from database import Database
from cliente import cliente
from sucursal import sucursal
from ciudad import ciudad
from bodega import bodega
from empleado import empleado
from producto import producto
from marca import marca
from venta import venta
from perfil import perfil


class App:
    def __init__(self, db):
        # Main window
        self.db = db
        self.root = tk.Tk ()
        # Algunas especificaciones de tamaño y título de la ventana
        self.root.geometry ( "950x550" )
        self.root.title ( "GOOD - TECH" )
        Inicio(self.db, self.root)
        # color de ventana

class Inicio:
    def __init__(self, db, root):
        self.db = db
        self.root = root
        self.root.config(background = "royalblue4")
        # creación de botones e imagen

        self.__agrega_imagen_principal ()
        self.__crea_botones_principales ()

        # Empieza a correr la interfaz.
        self.root.mainloop ()

    def __agrega_imagen_principal(self):
        #
        self.fondo = LabelFrame ( self.root, text="", relief=tk.FLAT )
        self.fondo.place ( x=0, y=0, relwidth=1, relheight=1 )
        image = Image.open ( "fondo.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (950, 550), Image.ANTIALIAS ) )
        self.label = Label ( self.fondo, image=photo )
        self.label.image = photo
        self.label.pack ()

        self.frame = LabelFrame ( self.root, text="", relief=tk.FLAT )
        self.frame.place ( x=170, y=30, relwidth=0.64, relheight=0.67 )
        image = Image.open ( "foto.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (610, 389), Image.ANTIALIAS ) )
        self.label = Label ( self.frame, image=photo )
        self.label.image = photo
        self.label.pack ()

    def __crea_botones_principales(self):
        self.b_in = tk.Button ( self.root, text="Ingresar", width=20, command=self.btn_hide)
        self.b_in.place ( x=373.39, y=425, width=205, height=48)
        self.b_in.bind ( '<Button-1>', administrador (self.db, self.root))
        #self.b_in.bind ( '<Button-1>', self.__login )
        self.b_in.config ( background="cyan4" )

    def btn_hide(self):
        self.b_in.place_forget ()

    def __login(self, button):
        self.label.master.destroy ()
        login (self.db, self.root)

class login:
    def __init__(self, db, root):
        self.db = db
        self.root = root

        sql = """delete from perfil"""
        self.db.run_sql ( sql, {""} )
        sql = """insert into perfil (id_perfil, tipo_perfil) values (1, "Administrador"), (2, "Admin Bodega"), (3, "Venta")"""
        self.db.run_sql ( sql, {""} )

        self.frame = LabelFrame ( self.root, text="" )
        self.frame.place ( x=330, y=53, relwidth=0.31, relheight=0.8 )
        self.fondo = LabelFrame ( self.frame, text="", relief=tk.FLAT )
        self.fondo.place ( x=0, y=0, relwidth=1, relheight=1)
        image = Image.open ( "login.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (840, 440), Image.ANTIALIAS ) )
        self.label = Label ( self.fondo, image=photo )
        self.label.image = photo
        self.label.pack ()

        #Contenido Ventana
        self.__config_entry()
        self.__config_buttons()

    #Configuración de las casillas que el usuario ingresa info
    def __config_entry(self):
        self.entry_user = ttk.Combobox(self.frame)
        self.entry_user.place(x = 126, y = 295.6, width = 133, height = 20)
        self.entry_user["values"], self.__user = self.__fill_combo_user ()
        self.entry_pass = ttk.Entry ( self.frame, show="*" )
        self.entry_pass.place ( x=126, y=327.1, width=133, height=20 )

    def __fill_combo_user(self):
        sql = "select id_perfil, tipo_perfil from perfil order by id_perfil asc"
        self.data = self.db.run_select ( sql )
        return [i[1] for i in self.data], [i[0] for i in self.data]

    #Configuración de los botones
    def __config_buttons(self):
        ttk.Button(self.frame, text="Aceptar", command = self.__eleccion).place ( x=95, y=370, width=105, height=25 )

    def __eleccion(self):
        if(self.entry_user.get() == self.data[0][1]):
            if (self.entry_pass.get() != "admin"):
               self.mensaje()
            else:
                self.ufa()
        elif (self.entry_user.get () == self.data[1][1]):
            if (self.entry_pass.get () != "bodega"):
                self.mensaje ()
            else:
                self.ufa ()
        elif (self.entry_user.get () == self.data[2][1]):
            if (self.entry_pass.get () != "venta"):
                self.mensaje ()
            else:
                self.ufa ()

    def mensaje(self):
        messagebox.showinfo (self.root, message="Contraseña incorrecta" )

    def ufa(self):
        self.frame.place_forget ()
        administrador (self.db, self.root)

class administrador:
    def __init__(self, db, root):
        self.db = db
        self.root = root
        # creación de botones e imagen
        self.__agrega_imagen_principal ()
        self.__crea_botones_principales ()

    # botones principales.
    def __crea_botones_principales(self):
        padx = 2
        pady = 2

        self.b1 = Button ( self.root, text="Clientes", width=20)
        self.b1.place ( x = 30, y = 30)
        self.b1.bind ( '<Button-1>', self.__mostrar_clientes )


        self.b2 = Button ( self.root, text="Sucursales", width=20 )
        self.b2.place ( x = 30, y = 70)
        self.b2.bind ( '<Button-1>', self.__mostrar_sucursales )

        #
        self.b3 = Button ( self.root, text="Ciudades", width=20 )
        self.b3.place ( x = 30, y = 110)
        self.b3.bind ( '<Button-1>', self.__mostrar_ciudades )

        #
        self.b4 = Button ( self.root, text="Bodegas", width=20 )
        self.b4.place ( x = 30, y = 150)
        self.b4.bind ( '<Button-1>', self.__mostrar_bodegas )

        self.b5 = Button ( self.root, text="Empleados", width=20 )
        self.b5.place ( x = 30, y = 190)
        self.b5.bind ( '<Button-1>', self.__mostrar_empleados )


        self.b6 = Button ( self.root, text="Productos", width=20 )
        self.b6.place ( x = 30, y = 230)
        self.b6.bind ( '<Button-1>', self.__mostrar_productos )


        self.b7 = Button ( self.root, text="Marcas", width=20 )
        self.b7.place ( x = 30, y = 270)
        self.b7.bind ( '<Button-1>', self.__mostrar_marcas )


        self.b8 = Button ( self.root, text="Venta", width=20 )
        self.b8.place ( x = 30, y = 310)
        self.b8.bind ( '<Button-1>', self.__mostrar_ventas )
        self.b8.config ( background="red" )


        self.b9 = Button ( self.root, text="Perfil", width=20 )
        self.b9.place ( x = 30, y = 350)
        self.b9.bind ( '<Button-1>', self.__mostrar_perfil )
        self.b9.config ( background="red" )


        self.b_atras = ttk.Button ( self.root, text="Cerrar sesión", width=20, command= self.btn_hide )
        self.b_atras.place ( x = 40, y = 490)
        self.b_atras.bind ( '<Button-1>', self.__atras )


        self.__botones_dorados()

    def btn_hide(self):
        self.b_atras.place_forget ()

    # imagen principal.
    def __agrega_imagen_principal(self):
        #
        self.fondo = LabelFrame ( self.root, text="", relief=tk.FLAT )
        self.fondo.place ( x=0, y=0, relwidth=1, relheight=1 )
        image = Image.open ( "fondo2.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (950, 550), Image.ANTIALIAS ) )
        self.label = Label ( self.fondo, image=photo )
        self.label.image = photo
        self.label.pack ()

    def __mostrar_clientes(self, button):
        self.__limpia_pantalla()
        cliente ( self.root, self.db, self.b1, self.__limpia_pantalla)

    def __mostrar_sucursales(self, button):
        self.__limpia_pantalla()
        sucursal ( self.root, self.db, self.b2, self.__limpia_pantalla)

    def __mostrar_ciudades(self, button):
        self.__limpia_pantalla()
        ciudad ( self.root, self.db, self.b3, self.__limpia_pantalla)

    def __mostrar_bodegas(self, button):
        self.__limpia_pantalla()
        bodega ( self.root, self.db, self.b4, self.__limpia_pantalla )

    def __mostrar_empleados(self, button):
        self.__limpia_pantalla()
        empleado ( self.root, self.db, self.b5, self.__limpia_pantalla )

    def __mostrar_productos(self, button):
        self.__limpia_pantalla()
        producto ( self.root, self.db, self.b6, self.__limpia_pantalla )

    def __mostrar_marcas(self, button):
        self.__limpia_pantalla()
        marca ( self.root, self.db, self.b7, self.__limpia_pantalla )

    def __mostrar_ventas(self, button):
        self.__limpia_pantalla()
        venta ( self.root, self.db )

    def __mostrar_perfil(self, button):
        self.__limpia_pantalla()
        perfil(self.root, self.db )


    def __atras(self, button):
        ke_dijo = messagebox.askyesno ( message="¿Desea cerrar sesión?" )
        if (ke_dijo == True):
            self.label.master.destroy ()
            self.b1.place_forget ()
            Inicio(self.db, self.root)


    def __limpia_pantalla(self):
        self.label.master.destroy ()
        self.__agrega_imagen_principal()
        self.__crea_botones_principales()


    def __botones_dorados(self):
        self.b1.config ( background="dark goldenrod" )
        self.b2.config ( background="dark goldenrod" )
        self.b3.config ( background="dark goldenrod" )
        self.b4.config ( background="dark goldenrod" )
        self.b5.config ( background="dark goldenrod" )
        self.b6.config ( background="dark goldenrod" )
        self.b7.config ( background="dark goldenrod" )
        #self.b8.config ( background="dark goldenrod" )
        #self.b9.config ( background="dark goldenrod" )




class adm_bodega:
    def __init__(self, db, root):
        self.db = db
        self.root = root
        # creación de botones e imagen
        self.__agrega_imagen_principal ()
        self.__crea_botones_principales ()


    # botones principales.
    def __crea_botones_principales(self):
        padx = 2
        pady = 2

        #
        self.b1 = Button ( self.root, text="Clientes", width=20 )
        self.b1.place ( x = 30, y = 30)
        self.b1.bind ( '<Button-1>', self.__mostrar_clientes )
        self.b1.config ( background="dark goldenrod" )

        #
        b2 = Button ( self.root, text="Sucursales", width=20 )
        b2.place ( x = 30, y = 70)
        b2.bind ( '<Button-1>', self.__mostrar_sucursales )
        b2.config ( background="dark goldenrod" )

        #
        b3 = Button ( self.root, text="Ciudades", width=20 )
        b3.place ( x = 30, y = 110)
        b3.bind ( '<Button-1>', self.__mostrar_ciudades )
        b3.config ( background="dark goldenrod" )

        #
        b4 = Button ( self.root, text="Bodegas", width=20 )
        b4.place ( x = 30, y = 150)
        b4.bind ( '<Button-1>', self.__mostrar_bodegas )
        b4.config ( background="dark goldenrod" )

        b5 = Button ( self.root, text="Empleados", width=20 )
        b5.place ( x = 30, y = 190)
        b5.bind ( '<Button-1>', self.__mostrar_empleados )
        b5.config ( background="dark goldenrod" )

        b6 = Button ( self.root, text="Productos", width=20 )
        b6.place ( x = 30, y = 230)
        b6.bind ( '<Button-1>', self.__mostrar_productos )
        b6.config ( background="dark goldenrod" )

        b7 = Button ( self.root, text="Marcas", width=20 )
        b7.place ( x = 30, y = 270)
        b7.bind ( '<Button-1>', self.__mostrar_marcas )
        b7.config ( background="dark goldenrod" )

        b8 = Button ( self.root, text="Venta", width=20 )
        b8.place ( x = 30, y = 310)
        # b8.bind ( '<Button-1>', self. )
        b8.config ( background="red" )

        b9 = Button ( self.root, text="Detalle venta", width=20 )
        b9.place ( x = 30, y = 350)
        # b9.bind ( '<Button-1>', self. )
        b9.config ( background="red" )

        self.b_atras = Button ( self.root, text="Cerrar sesión", width=20, command= self.btn_hide )
        self.b_atras.place ( x = 30, y = 490)
        self.b_atras.bind ( '<Button-1>', self.__atras )
        self.b_atras.config ( background="red" )

    def btn_hide(self):
        self.b_atras.place_forget ()



    # imagen principal.
    def __agrega_imagen_principal(self):
        #
        self.fondo = LabelFrame ( self.root, text="", relief=tk.FLAT )
        self.fondo.place ( x=0, y=0, relwidth=1, relheight=1 )
        image = Image.open ( "fondo2.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (950, 550), Image.ANTIALIAS ) )
        self.label = Label ( self.fondo, image=photo )
        self.label.image = photo
        self.label.pack ()

    def __mostrar_clientes(self, button):
        cliente ( self.root, self.db )

    def __mostrar_sucursales(self, button):
        sucursal ( self.root, self.db )

    def __mostrar_ciudades(self, button):
        ciudad ( self.root, self.db )

    def __mostrar_bodegas(self, button):
        bodega ( self.root, self.db )

    def __mostrar_empleados(self, button):
        empleado ( self.root, self.db )

    def __mostrar_productos(self, button):
        producto ( self.root, self.db )

    def __mostrar_marcas(self, button):
        marca ( self.root, self.db )

    def __atras(self, button):
        self.label.master.destroy ()
        self.b1.place_forget ()

        Inicio(self.db, self.root)






def main():
    # Conecta a la base de datos
    db = Database ()
    App (db)

if __name__ == "__main__":
    main ()
