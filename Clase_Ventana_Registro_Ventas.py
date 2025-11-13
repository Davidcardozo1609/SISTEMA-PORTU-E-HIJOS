#___________LIBERIAS___________________
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos  
from Plantilla import Clase_Plantilla
import customtkinter as ctk
import tkinter as tk 
from tksheet import Sheet #permite hacer la tabla
from datetime import datetime
from tkinter import ttk

#___________CLASE COMPRAS___________________
class Registro_Ventas(Clase_Plantilla):
    def __init__(self,master,titulo="Registro De Ventas",ventana_padre=None,ventana_login=None,usuario_actual=None,parent_app=None,no_abrir_ventana=None):
        
        
                #En el init se definen las cosas que se van a ejecutar al instanciar la clase
                #entre parentesis ponemos lo que va a recibir,etc. algunos  estan en None para que
                #al no recibir ese valor no se rompa, por ejemplo compras no hace falta que le pasa un parent
                #pero si no le paso un master se rompe."""
                        
       
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app,
                 no_abrir_ventana=no_abrir_ventana)
        

        self.bd = BaseDeDatos()
                #MUY IMPORTANTE: Llama al init de plantilla permitiendo tener las cosas de plantilla
                #Labels,Entrys,Frames,etc. Pero plantilla para ejecutar eso necesita que le pases
                #las cosas entre (), entonces lo que hacemos es pasarle las cosas de nuestro init a plantilla
        
        
        
        
#_______________________________FRAMES_____________________________________
        
        #Fr_Gris (ayuda a hacer el borde)
        self.Fr_help_ventas = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")
        self.Fr_help_ventas.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.65)
        
        #Fr_Blanco el principal
        self.Fr_blanco_ventas = ctk.CTkFrame(self.Fr_help_ventas,
                                                fg_color="#ffffff" 
                                                )
        self.Fr_blanco_ventas.place(relx=0.002, rely=0.002, relwidth=0.996, relheight=0.996)
        
        
        
    

        # Crear la tabla
        self.crear_tabla(
            self.Fr_blanco_ventas,  # frame donde irá la tabla
            columnas=["ID","Fecha","Total"],
            con_acciones=False,
            detalles=True

        )
        
        self.actualizar_tabla()
        

        #Label Titulo
        self.Lbl_nombre_modulo.configure(text="Registro de Ventas")
        self.Lbl_nombre_modulo.place(relx=0.1,rely=0.03,relwidth=0.43,relheight=0.1)
        
        self.tree.bind("<Button-1>", self.click_en_tabla)
        
        
        
        self.Ventas = ctk.CTkButton(
            self.Fr_Principal,
            text="+ Nuevo Registro",
            fg_color="blue",
            hover_color="blue",
            font=("Arial", 20),
            command=lambda: self.ir_a_pantalla_x(
                                   __import__("Clase_Ventana_Ventas").Ventas,  # 👈 import diferido
                                   master=self.ventana,
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=self
            ))
        
        
        self.Ventas.place(relx=0.1, rely=0.85, relwidth=0.2, relheight=0.07)
        
        
        
    def actualizar_tabla(self):
        # Limpiar la tabla primero
        for fila in self.tree.get_children():
            self.tree.delete(fila)
            
        self.bd.cursor.execute(
        """SELECT id, fecha, total FROM registro_ventas"""
        
        )
        resultado = self.bd.cursor.fetchall()
        
        for fila in resultado:
            valores = list(fila)  
            valores += ["Detalles"]  # Añadimos botones de acción
            self.tree.insert("", "end", values=valores)
            
            
    def click_en_tabla(self, event):
        item = self.tree.identify_row(event.y)
        columna = self.tree.identify_column(event.x)

        if not item:
            return

        fila_id = self.tree.item(item, "values")

        # Si la columna es la de "Detalles"
        if columna == "#4":  # Ajustá el número de columna según tu tabla
            self.ventana_detalles(fila_id)

            
            
    def ventana_detalles(self, fila_id):
        try:
            venta_id = fila_id[0]
        except (IndexError, TypeError):
            ms.showwarning("Aviso", "No se seleccionó ninguna compra.")
            return

        # Crear ventana independiente
        ventana_detalle = ctk.CTkToplevel(self.ventana)
        ventana_detalle.title(f"Detalles de Ventas #{venta_id}")
        ventana_detalle.geometry("700x400")
        ventana_detalle.resizable(False, False)
        ventana_detalle.grab_set()

        # Crear tabla dentro de la nueva ventana
        frame_tabla = ctk.CTkFrame(ventana_detalle)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ["Producto", "Cantidad","Precio","Tipo Pago", "Pago"]
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True)

        # Consultar los datos de la compra
        self.bd.cursor.execute("""
            SELECT productos, cantidad, precio, tipo_pago, pago
            FROM detalle_ventas
            WHERE ventas_id = ?
        """, (venta_id,))
        resultado = self.bd.cursor.fetchall()

        if not resultado:
            ms.showinfo("Detalles", "No hay detalles para esta Venta.",)
            return

        for fila in resultado:
            tree.insert("", "end", values=fila)
        