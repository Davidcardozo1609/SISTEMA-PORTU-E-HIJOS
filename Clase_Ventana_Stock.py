#LIBRERIAS
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import re
from tkcalendar import Calendar
from datetime import datetime, date
import sys, os
from tkinter import simpledialog
import shutil
from bd import BaseDeDatos
from Constantes import ICONO_FLECHA
from Clase_Editar_Producto import EditarProducto
from Plantilla import Clase_Plantilla
import customtkinter as ctk
from tksheet import Sheet #permite hacer la tabla

# --- PRODUCTOS --- #

class Productos(Clase_Plantilla):
    def __init__(self, master,titulo,ventana_padre,ventana_login,usuario_actual=None,parent_app=None,no_abrir_ventana=True):
        super().__init__(master=master, titulo=titulo,
                         ventana_padre=ventana_padre,ventana_login=ventana_login,
                         usuario_actual=usuario_actual,
                         parent_app=parent_app,
                         no_abrir_ventana=no_abrir_ventana)
        
        
         
#_________________________ FRAMES___________________________
        
        # Frame de Registro de ventas
       
        self.Lbl_nombre_modulo.configure(text="Productos")

        self.Lbl_nombre_modulo.place(relx=0.05,rely=0.03,relwidth=0.2,relheight=0.1)
        

    
        #Fr_Gris (ayuda a hacer el borde)
        self.Fr_help_productos = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")
        self.Fr_help_productos.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.58)
        
        #Fr_Blanco el principal
        self.Fr_blanco_productos = ctk.CTkFrame(self.Fr_help_productos,
                                                fg_color="#ffffff" 
                                                )
        self.Fr_blanco_productos.place(relx=0.002, rely=0.002, relwidth=0.996, relheight=0.996)
        


        
        self.crear_tabla(
            self.Fr_blanco_productos,  # frame donde irá la tabla
             columnas=["id", "Producto","Categoria","Cantidad","Precio_Unitario","Subtotal"],
            con_acciones=True

        )
        
        self.actualizar_tabla()
        
        
    # Insertar cada fila en el Treeview
    def actualizar_tabla(self):
        # Limpiar la tabla primero
        for fila in self.tree.get_children():
            self.tree.delete(fila)
            
        self.bd.cursor.execute(
        """SELECT * FROM productos_stock


        """
        
        )
        resultado = self.bd.cursor.fetchall()
        for fila in resultado:
            # Suponiendo que tus columnas en Treeview son:
            # ["Producto","Categoria","Cantidad","Precio_Unitario","Subtotal","Editar","Eliminar"]
            valores = list(fila[0:6])  # Tomamos solo producto, categoria, cantidad, precio_unitario, subtotal
            valores += ["Editar", "Eliminar"]  # Añadimos botones de acción
            self.tree.insert("", "end", values=valores)
                
    

        
        
        
        
        
        
        
        
 