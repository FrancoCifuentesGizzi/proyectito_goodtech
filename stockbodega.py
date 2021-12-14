import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import messagebox

class stockbodega:
    def __init__(self, root, db, bb6, __limpia_pantalla):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []
        self.root = root
        self.boton = bb6
        self.boton.config ( background="cyan" )
        self.__limpia_pantalla = __limpia_pantalla

        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_label(self):
        # Definición de entradas de texto
        self.suc_lab = ttk.Label(self.root, text = "")
        self.suc_lab.place(x = 300, y = 26, width = 500, height = 100)
        Label ( self.suc_lab, text="Bodega: " ).place ( x=30, y=30, width=80, height=20 )

    def __config_entry(self):
        self.combo = ttk.Combobox(self.suc_lab)
        self.combo.place(x = 97, y = 30, width = 150, height= 20)
        self.combo["values"], self.ids = self.__combo_suc()

    def __combo_suc(self):
        row_data = """select id_bodega, nombre_bod from bodega;"""
        self.data = self.db.run_select(row_data)
        # Se muestran los titulos de los libros para seleccionarlos
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # ver las editoriales
        btn_ok = ttk.Button(self.suc_lab, text = "Ver tabla-view",
            command = self.vista)
        btn_ok.place(x = 255, y = 10, width = 90, height = 30)

        # cancelar
        btn_cancel = ttk.Button(self.suc_lab, text = "Cancelar",
            command = self.cerrar_personal)
        btn_cancel.place(x = 255, y = 40, width = 90, height = 30)

    def vista(self):
        sql = """create or replace view view_bodega_stock as select bodega.nombre_bod, sum(stock_producto.stock) as stock 
            from stock_producto join bodega on stock_producto.bodega_id_bodega = bodega.id_bodega
            where bodega_id_bodega = %(id_bod)s"""

        self.db.run_sql(sql, {"id_bod": self.ids[self.combo.current()]})

        personal_venta(self.db, self.root)

    def cerrar_personal(self):
        self.boton.config ( background="dark goldenrod" )
        self.suc_lab.place_forget ()
        self.__limpia_pantalla ()


class personal_venta:
    def __init__(self, db, root):
        self.db = db
        self.data = []
        self.root = root

        self.__config_treeview_vista()
        self.llenar_treeview_vista()


    def __config_treeview_vista(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(columns = ("#0", "#1",))
        self.treeview.heading("#0", text = "Bodega")
        self.treeview.heading("#1", text = "Total stock")
        self.treeview.column("#0", minwidth = 200, width = 250, stretch = False)
        self.treeview.column("#1", minwidth = 200, width = 250, stretch = False)
        self.treeview.place(x = 300, y = 130, height = 300, width = 500)
        self.llenar_treeview_vista()
        self.root.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        row_data = """select nombre_bod, stock from view_bodega_stock;"""
        data = self.db.run_select(row_data)

        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", text = i[0],
                    values = (i[1], i[1]), iid = i[0])

            self.data = data