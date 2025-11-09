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
class Registro_Compras(Clase_Plantilla):
    def __init__(self,master,titulo="Compras",ventana_padre=None,ventana_login=None,usuario_actual=None,parent_app=None,no_abrir_ventana=None):
        
        
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
        self.Fr_help_compras = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")
        self.Fr_help_compras.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.65)
        
        #Fr_Blanco el principal
        self.Fr_blanco_compras = ctk.CTkFrame(self.Fr_help_compras,
                                                fg_color="#ffffff" 
                                                )
        self.Fr_blanco_compras.place(relx=0.002, rely=0.002, relwidth=0.996, relheight=0.996)
        
        
        
    

        # Crear la tabla
        self.crear_tabla(
            self.Fr_blanco_compras,  # frame donde irá la tabla
            columnas=["ID", "Proveedor","Fecha","Total"],
            con_acciones=True,
            detalles=True

        )
        
        self.actualizar_tabla()
        

        #Label Titulo
        self.Lbl_nombre_modulo.configure(text="Registro de Compras")
        self.Lbl_nombre_modulo.place(relx=0.1,rely=0.03,relwidth=0.35,relheight=0.1)
        
        self.tree.bind("<Button-1>", self.click_en_tabla)
        
        
        
        self.Compras = ctk.CTkButton(
            self.Fr_Principal,
            text="+ Nuevo Registro",
            fg_color="blue",
            hover_color="blue",
            font=("Arial", 20),
            command=lambda: self.ir_a_pantalla_x(
                                   __import__("Clase_Ventana_Compras").Compras,  # 👈 import diferido

                                   master=self.ventana,
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=self
            ))
        
        
        self.Compras.place(relx=0.1, rely=0.92, relwidth=0.2, relheight=0.07)
        
        
        
    def actualizar_tabla(self):
        # Limpiar la tabla primero
        for fila in self.tree.get_children():
            self.tree.delete(fila)
            
        self.bd.cursor.execute(
        """SELECT id, proveedor, fecha, total FROM registro_compras"""
        
        )
        resultado = self.bd.cursor.fetchall()
        
        for fila in resultado:
            valores = list(fila)  
            valores += ["Detalles","Editar", "Eliminar"]  # Añadimos botones de acción
            self.tree.insert("", "end", values=valores)
            
    def ventana_detalles(self, fila_id):
        compra_id = fila_id[0]  # el id de la compra

        # Crear ventana secundaria
        self.ventana_menu = ctk.CTkToplevel(self.ventana)
        self.ventana_menu.title(f"Detalles de la compra #{compra_id}")
        self.ventana_menu.geometry("700x400")
        self.ventana_menu.resizable(False, False)
        self.ventana_menu.grab_set()

        # Encabezado
        titulo = ctk.CTkLabel(self.ventana_menu, text=f"Detalles de la compra #{compra_id}", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        # Crear tabla
        self.crear_tabla(
            self.ventana_menu,
            columnas=["Producto", "Categoría", "Cantidad", "Precio_Unitario", "Subtotal"],
            con_acciones=False,
        )

        # Consulta SQL CORRECTA (coma entre columnas)
        self.bd.cursor.execute("""
            SELECT producto, categoria, cantidad, precio_unitario, subtotal
            FROM detalle_compras
            WHERE compra_id = ?
        """, (compra_id,))
        resultado = self.bd.cursor.fetchall()

        # Insertar filas en la tabla
        for fila in resultado:
            self.tree.insert("", "end", values=fila)
            
    def click_en_tabla(self, event):
        item = self.tree.identify_row(event.y)
        columna = self.tree.identify_column(event.x)

        if not item:
            return

        fila_id = self.tree.item(item, "values")

        # Si la columna es la de "Detalles"
        if columna == "#5":  # Ajustá el número de columna según tu tabla
            self.ventana_detalles(fila_id)

            
            
    def ventana_detalles(self, fila_id):
        try:
            compra_id = fila_id[0]
        except (IndexError, TypeError):
            ms.showwarning("Aviso", "No se seleccionó ninguna compra.")
            return

        # Crear ventana independiente
        ventana_detalle = ctk.CTkToplevel(self.ventana)
        ventana_detalle.title(f"Detalles de compra #{compra_id}")
        ventana_detalle.geometry("700x400")
        ventana_detalle.resizable(False, False)
        ventana_detalle.grab_set()

        # Crear tabla dentro de la nueva ventana
        frame_tabla = ctk.CTkFrame(ventana_detalle)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ["Producto", "Categoría", "Cantidad", "Precio Unitario", "Subtotal"]
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True)

        # Consultar los datos de la compra
        self.bd.cursor.execute("""
            SELECT producto, categoria, cantidad, precio_unitario, subtotal
            FROM detalle_compras
            WHERE compra_id = ?
        """, (compra_id,))
        resultado = self.bd.cursor.fetchall()

        if not resultado:
            ms.showinfo("Detalles", "No hay detalles para esta compra.")
            return

        for fila in resultado:
            tree.insert("", "end", values=fila)
            
        



            
    
        
        

        
        
    
            
    
        
        