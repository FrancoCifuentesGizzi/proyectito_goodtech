import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox
import matplotlib.pyplot as plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class grafo2:
    def __init__(self, root, db, bv5, __limpia_pantalla):
        self.root = root
        self.db = db
        self.__limpia_pantalla = __limpia_pantalla
        self.root = root
        self.boton = bv5
        self.boton.config ( background="cyan" )

        # se llama a la funcion que permite la configuracion de la grafica
        self.__config_grafica ()

    # Se define la funcion de la configuracion de grafica
    def __config_grafica(self):
        # Figura que hara el plot
        figura_canva, ax = plot.subplots ()
        x, y = self.obtencion_datos ()
        # Titulo
        plot.title ( "Histograma: Ventas realizadas por empleados" )
        # Nombre del eje X
        plot.xlabel ( "Empleados" )
        # Nombre del eje Y
        plot.ylabel ( "Total de ventas realizadas" )
        # Color de las barras
        plot.bar ( x, y, color="purple" )
        self.label = LabelFrame ( self.root, text="" )
        self.label.place ( x=189, y=26, width=735, height=500 )
        self.canvas = tk.Canvas ( self.label, width=600, height=350, )
        self.canvas.place ( x=210, y=26 )
        self.canvas = FigureCanvasTkAgg ( figura_canva, master=self.label )
        self.canvas.draw ()
        self.canvas.get_tk_widget ().pack ()
        self.botoncito ()

    # Funcion que permite obtener los datos desde sql
    def obtencion_datos(self):
        sql = """select empleado.nombre_emp, count(*) from empleado
        inner join venta on empleado.id_empleado = venta.empleado_id_empleado
        group by empleado.nombre_emp;"""

        data = self.db.run_select ( sql )
        # el eje X
        x = [i[0] for i in data]
        # el eje Y
        y = [i[1] for i in data]
        return x, y

    def botoncito(self):
        ttk.Button ( self.label, text="Cerrar",
                     command=self.__Cerrar_G ).place ( x=627, y=470, width=100, height=25 )

    def __Cerrar_G(self):
        plot.close ()
        self.boton.config ( background="dark goldenrod" )
        self.label.place_forget ()
        self.__limpia_pantalla ()
        # self.label.destroy ()
