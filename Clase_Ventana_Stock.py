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
       
        self.Lbl_nombre_modulo.destroy()
        
        self.fr_borde=ctk.CTkFrame(self.Fr_Principal, fg_color="grey")
        self.fr_borde.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        #frame principal
        
        self.fr_blanco=ctk.CTkFrame(self.fr_borde, fg_color="white")
        self.fr_blanco.place(relx=0.004, rely=0.004, relwidth=0.992, relheight=0.992)
        
        #Fr_Gris (ayuda a hacer el borde)
        self.Fr_help_compras = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")
        self.Fr_help_compras.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.6)
        
        #Fr_Blanco el principal
        self.Fr_blanco_compras = ctk.CTkFrame(self.Fr_help_compras,
                                                fg_color="#ffffff" 
                                                )
        self.Fr_blanco_compras.place(relx=0.002, rely=0.002, relwidth=0.996, relheight=0.996)
        


        
        self.crear_tabla(
            self.Fr_blanco_compras,  # frame donde irá la tabla
             columnas=["id", "Producto","Categoria","Cantidad","Precio_Unitario","Subtotal"],
            con_acciones=True

        )
        
        self.actualizar_tabla()
        
             
        
        
        # APARTADO DE LABELS  
        
        #Titulo de productos
        
        self.lbl_producto= ctk.CTkLabel(self.fr_blanco,text="Productos", fg_color="white", anchor="w", text_color="black", font=("carme", 36))
        self.lbl_producto.place(relx=0.03 ,rely=0.035 ,relwidth=0.5 ,relheight=0.105)
        
        # Apartado de Botones
       
        


        
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
                
    

        
        
        
        
        
        
        
        
 