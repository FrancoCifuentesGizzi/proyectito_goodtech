import tkinter as tk
import tkinter as ttk
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk

from database import Database
from cliente import cliente
from sucursal import sucursal
from ciudad import ciudad
from bodega import bodega
from empleado import empleado
from producto import producto
from marca import marca
from app import app


class administrador:
    def __init__(self, db, root):
        self.db = db
        self.root = root
        # Main window

        self.root.config ( background="goldenrod" )

        # creación de botones e imagen
        self.__crea_botones_principales ()
        self.__agrega_imagen_principal ()

        # Empieza a correr la interfaz.
        self.root.mainloop ()

    # botones principales.
    def __crea_botones_principales(self):
        padx = 2
        pady = 2

        #
        frame = LabelFrame ( self.root, text="Opciones de administrador", relief=tk.GROOVE )
        frame.place ( x=30, y=10, width=160, relheight=0.95 )
        frame.config ( background="goldenrod" )

        #
        b1 = Button ( frame, text="Clientes", width=20 )
        b1.grid ( row=0, column=0, padx=padx, pady=pady )
        b1.bind ( '<Button-1>', self.__mostrar_clientes )
        b1.config ( background="dark goldenrod" )

        #
        b2 = Button ( frame, text="Sucursales", width=20 )
        b2.grid ( row=1, column=0, padx=padx, pady=pady )
        b2.bind ( '<Button-1>', self.__mostrar_sucursales )
        b2.config ( background="dark goldenrod" )

        #
        b3 = Button ( frame, text="Ciudades", width=20 )
        b3.grid ( row=2, column=0, padx=padx, pady=pady )
        b3.bind ( '<Button-1>', self.__mostrar_ciudades )
        b3.config ( background="dark goldenrod" )

        #
        b4 = Button ( frame, text="Bodegas", width=20 )
        b4.grid ( row=3, column=0, padx=padx, pady=pady )
        b4.bind ( '<Button-1>', self.__mostrar_bodegas )
        b4.config ( background="dark goldenrod" )


        b5 = Button ( frame, text="Empleados", width=20 )
        b5.grid ( row=4, column=0, padx=padx, pady=pady )
        b5.bind ( '<Button-1>', self.__mostrar_empleados )
        b5.config ( background="dark goldenrod" )

        b6 = Button ( frame, text="Productos", width=20 )
        b6.grid ( row=5, column=0, padx=padx, pady=pady )
        b6.bind ( '<Button-1>', self.__mostrar_productos )
        b6.config ( background="dark goldenrod" )

        b7 = Button ( frame, text="Marcas", width=20 )
        b7.grid ( row=6, column=0, padx=padx, pady=pady )
        b7.bind ( '<Button-1>', self.__mostrar_marcas )
        b7.config ( background="dark goldenrod" )

        b8 = Button ( frame, text="Venta", width=20 )
        b8.grid ( row=7, column=0, padx=padx, pady=pady )
        # b8.bind ( '<Button-1>', self. )
        b8.config ( background="red" )

        b9 = Button ( frame, text="Detalle venta", width=20 )
        b9.grid ( row=8, column=0, padx=padx, pady=pady )
        # b9.bind ( '<Button-1>', self. )
        b9.config ( background="red" )

        b_atras = Button ( frame, text="Detalle venta", width=20 )
        b_atras.place ( row=500, column=400, width=150)
        b_atras b9.bind ( '<Button-1>', self. )
        b9.config ( background="red" )





    # imagen principal.
    def __agrega_imagen_principal(self):
        #
        frame = LabelFrame ( self.root, text="", relief=tk.FLAT )
        frame.place ( x=220, y=10, relwidth=0.6, relheight=0.7 )

        image = Image.open ( "admin.jpg" )
        photo = ImageTk.PhotoImage ( image.resize ( (450, 300), Image.ANTIALIAS ) )
        label = Label ( frame, image=photo )
        label.image = photo
        label.pack ()

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
        __crea


def main():
    # Conecta a la base de datos
    db = Database ()
    # La app xD
    administrador ( db )


if __name__ == "__main__":
    main ()