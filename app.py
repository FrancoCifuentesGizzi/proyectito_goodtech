import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk
from tkinter import messagebox
import matplotlib.pyplot as plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from database import Database
from cliente import cliente
from sucursal import sucursal
from ciudad import ciudad
from bodega import bodega
from empleado import empleado
from producto import producto
from marca import marca
from venta import venta
from stock_producto import stock_producto
from perfil import perfil
from personal import personal
from grafo1 import grafo1
from grafo2 import grafo2
from stockbodega import stockbodega



class App:
    def __init__(self, db):
        # Main window
        self.db = db
        self.root = tk.Tk ()

        self.root.title ( "GOOD - TECH" )        # Algunas especificaciones de tamaño y título de la ventana
        self.root.geometry ( "950x550" )
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
        self.b_in.bind ( '<Button-1>', self.__login )
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

        sql = """insert into perfil (id_perfil, tipo_perfil) values (1, "Administrador"), (2, "Admin Bodega"), (3, "Venta")"""
        self.db.corre_user_sql ( sql )

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
                self.__admin()
        elif (self.entry_user.get () == self.data[1][1]):
            if (self.entry_pass.get () != "bodega"):
                self.mensaje ()
            else:
                self.__bodega ()
        elif (self.entry_user.get () == self.data[2][1]):
            if (self.entry_pass.get () != "venta"):
                self.mensaje ()
            else:
                self.__venta ()

    def mensaje(self):
        messagebox.showinfo (self.root, message="Contraseña incorrecta" )

    def __admin(self):
        self.frame.place_forget ()
        administrador (self.db, self.root)

    def __bodega(self):
        self.frame.place_forget ()
        admin_bodega (self.db, self.root)

    def __venta(self):
        self.frame.place_forget ()
        ventass(self.db, self.root)

class administrador:
    def __init__(self, db, root):
        self.db = db
        self.root = root
        # creación de botones e imagen
        self.__agrega_imagen_principal ()
        self.__crea_botones_principales ()

        # botones principales.
    def __crea_botones_principales(self):

        self.b1 = Button ( self.root, text="Clientes", width=20)
        self.b1.place ( x = 30, y = 30)
        self.b1.bind ( '<Button-1>', self.__mostrar_clientes )

        self.b2 = Button ( self.root, text="Sucursales", width=20 )
        self.b2.place ( x = 30, y = 65)
        self.b2.bind ( '<Button-1>', self.__mostrar_sucursales )
        #
        self.b3 = Button ( self.root, text="Ciudades", width=20 )
        self.b3.place ( x = 30, y = 100)
        self.b3.bind ( '<Button-1>', self.__mostrar_ciudades )
        #
        self.b4 = Button ( self.root, text="Bodegas", width=20 )
        self.b4.place ( x = 30, y = 135)
        self.b4.bind ( '<Button-1>', self.__mostrar_bodegas )

        self.b5 = Button ( self.root, text="Empleados", width=20 )
        self.b5.place ( x = 30, y = 170)
        self.b5.bind ( '<Button-1>', self.__mostrar_empleados )

        self.b6 = Button ( self.root, text="Productos", width=20 )
        self.b6.place ( x = 30, y = 205)
        self.b6.bind ( '<Button-1>', self.__mostrar_productos )

        self.b7 = Button ( self.root, text="Marcas", width=20 )
        self.b7.place ( x = 30, y = 240)
        self.b7.bind ( '<Button-1>', self.__mostrar_marcas )

        self.b8 = Button ( self.root, text="Venta", width=20 )
        self.b8.place ( x = 30, y = 275)
        self.b8.bind ( '<Button-1>', self.__mostrar_ventas )

        self.b9 = Button ( self.root, text="Stock Producto", width=20 )
        self.b9.place ( x=30, y=310 )
        self.b9.bind ( '<Button-1>', self.__mostrar_stock )

        self.b10 = Button ( self.root, text="Perfiles", width=20 )
        self.b10.place ( x=30, y=345 )
        self.b10.bind ( '<Button-1>', self.__mostrar_perfil )

        self.b11 = Button ( self.root, text="Ventas de Personal", width=20 )
        self.b11.place ( x=30, y=380 )
        self.b11.bind ( '<Button-1>', self.__ver_personal)

        self.b12 = Button ( self.root, text="Gráfico sucursales", width=20 )
        self.b12.place ( x=30, y=415 )
        self.b12.bind ( '<Button-1>', self.__ver_grafo1)


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
        venta ( self.root, self.db, self.b8, self.__limpia_pantalla )

    def __mostrar_stock(self, button):
        self.__limpia_pantalla()
        stock_producto ( self.root, self.db, self.b9, self.__limpia_pantalla )

    def __mostrar_perfil(self, button):
        self.__limpia_pantalla()
        perfil(self.root, self.db, self.b10, self.__limpia_pantalla)

    def __ver_personal(self, button):
        self.__limpia_pantalla ()
        personal(self.root, self.db, self.b11, self.__limpia_pantalla)

    def __ver_grafo1(self, button):
        self.__limpia_pantalla ()
        grafo1(self.root, self.db, self.b12, self.__limpia_pantalla)


    def __atras(self, button):
        ke_dijo = messagebox.askyesno ( message="¿Desea cerrar sesión?" )
        if (ke_dijo == True):
            self.label.master.destroy ()
            self.b1.place_forget ()
            Inicio(self.db, self.root)

    def __limpia_pantalla(self):
        self.label.master.destroy ()
        plot.close ()
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
        self.b8.config ( background="dark goldenrod" )
        self.b9.config ( background="dark goldenrod" )
        self.b10.config ( background="dark goldenrod" )
        self.b11.config ( background="dark goldenrod" )
        self.b12.config ( background="dark goldenrod" )

class admin_bodega:
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

        self.bb3 = Button ( self.root, text="Productos", width=20 )
        self.bb3.place ( x = 30, y = 30)
        self.bb3.bind ( '<Button-1>', self.__mostrar_productos )

        self.bb4 = Button ( self.root, text="Marcas", width=20 )
        self.bb4.place ( x = 30, y = 65)
        self.bb4.bind ( '<Button-1>', self.__mostrar_marcas )

        self.bb5 = Button ( self.root, text="Stock Producto", width=20 )
        self.bb5.place ( x=30, y=100)
        self.bb5.bind ( '<Button-1>', self.__mostrar_stock )

        self.bb6 = Button ( self.root, text="Stock en bodega", width=20 )
        self.bb6.place ( x=30, y=135)
        self.bb6.bind ( '<Button-1>', self.__stockbodega )

        self.bb_atras = ttk.Button ( self.root, text="Cerrar sesión", width=20, command= self.btn_hide )
        self.bb_atras.place ( x = 40, y = 490)
        self.bb_atras.bind ( '<Button-1>', self.__atras )

        self.__botones_dorados()

    def btn_hide(self):
        self.bb_atras.place_forget ()

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

    def __mostrar_productos(self, button):
        self.__limpia_pantalla()
        producto ( self.root, self.db, self.bb3, self.__limpia_pantalla )

    def __mostrar_marcas(self, button):
        self.__limpia_pantalla()
        marca ( self.root, self.db, self.bb4, self.__limpia_pantalla )

    def __mostrar_stock(self, button):
        self.__limpia_pantalla()
        stock_producto ( self.root, self.db, self.bb5, self.__limpia_pantalla )

    def __stockbodega(self, button):
        self.__limpia_pantalla()
        stockbodega( self.root, self.db, self.bb6, self.__limpia_pantalla )

    def __atras(self, button):
        ke_dijo = messagebox.askyesno ( message="¿Desea cerrar sesión?" )
        if (ke_dijo == True):
            self.label.master.destroy ()
            self.bb3.place_forget ()
            Inicio(self.db, self.root)

    def __limpia_pantalla(self):
        self.label.master.destroy ()
        self.__agrega_imagen_principal()
        self.__crea_botones_principales()

    def __botones_dorados(self):
        self.bb3.config ( background="dark goldenrod" )
        self.bb4.config ( background="dark goldenrod" )
        self.bb5.config ( background="dark goldenrod" )
        self.bb6.config ( background="dark goldenrod" )


class ventass:
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

        self.bv1 = Button ( self.root, text="Clientes", width=20 )
        self.bv1.place ( x=30, y=30 )
        self.bv1.bind ( '<Button-1>', self.__mostrar_clientes )

        self.bv3 = Button ( self.root, text="Venta", width=20 )
        self.bv3.place ( x=30, y=65)
        self.bv3.bind ( '<Button-1>', self.__mostrar_ventas )

        self.bv5 = Button ( self.root, text="Gráfico ventas", width=20 )
        self.bv5.place ( x=30, y=100 )
        self.bv5.bind ( '<Button-1>', self.__ver_grafo2 )

        self.bv_atras = ttk.Button ( self.root, text="Cerrar sesión", width=20, command=self.btn_hide )
        self.bv_atras.place ( x=40, y=490 )
        self.bv_atras.bind ( '<Button-1>', self.__atras )

        self.__botones_dorados ()

    def btn_hide(self):
        self.bv_atras.place_forget ()

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
        self.__limpia_pantalla ()
        cliente ( self.root, self.db, self.bv1, self.__limpia_pantalla )

    def __mostrar_personal(self, button):
        self.__limpia_pantalla ()
        personal ( self.root, self.db, self.bv2, self.__limpia_pantalla )

    def __mostrar_ventas(self, button):
        self.__limpia_pantalla ()
        venta ( self.root, self.db, self.bv3, self.__limpia_pantalla )

    def __ver_grafo2(self, button):
        self.__limpia_pantalla ()
        grafo2 ( self.root, self.db, self.bv5, self.__limpia_pantalla )


    def __atras(self, button):
        ke_dijo = messagebox.askyesno ( message="¿Desea cerrar sesión?" )
        if (ke_dijo == True):
            self.label.master.destroy ()
            self.bv1.place_forget ()
            Inicio ( self.db, self.root )

    def __limpia_pantalla(self):
        self.label.master.destroy ()
        self.__agrega_imagen_principal ()
        self.__crea_botones_principales ()

    def __botones_dorados(self):
        self.bv1.config ( background="dark goldenrod" )
        self.bv3.config ( background="dark goldenrod" )
        #self.b4.config ( background="dark goldenrod" )
        self.bv5.config ( background="dark goldenrod" )




def main():
    # Conecta a la base de datos
    db = Database ()
    App (db)

if __name__ == "__main__":
    main ()
