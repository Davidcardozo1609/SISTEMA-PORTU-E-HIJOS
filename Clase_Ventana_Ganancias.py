#___________LIBRERIAS_______________
import sqlite3 as sqlcon
import tkinter as tk
from tkinter import messagebox as ms
import sys, os
import customtkinter as ctk
from Plantilla import Clase_Plantilla
from tkinter import ttk


# ABREVIACIONES/REFERENCIAS:


# - - - CLASE DE GANACIOAS - - - #


class Ganancias(Clase_Plantilla):
    
    def __init__(self,master=None, titulo="Ganancias",ventana_padre=None,ventana_login=None, usuario_actual=None,parent_app=None):
        
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
        
        self.ventana_padre = ventana_padre
        self.ventana_login = ventana_login
        self.usuario_actual = usuario_actual
        self.parent_app = parent_app
        
        ctk.set_appearance_mode("light")      # modo claro
        ctk.set_default_color_theme("blue")   # color principal por defecto

        self.Lbl_nombre_modulo.configure(text="Ganancias", anchor="w", fg_color="#fdfdfd")

        # Variables

        self.gastos = 0
        self.ventas = 0
        self.ganancias = 0

        # LABEL DE GASTOS

        # Label
        self.Fr_Gastos = ctk.CTkFrame(self.Fr_Principal, fg_color="LightGrey")
        self.Fr_Gastos.place(relx=0.6, rely=0.2, relwidth=0.35, relheight=0.2)

        # Texto
        self.txt_gastos = ctk.CTkLabel(self.Fr_Gastos, bg_color="transparent", text="Gastos", anchor="w", font=("Carme", 18))
        self.txt_gastos.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)

        # Variable
        self.txt_mostrar_gastos = ctk.CTkLabel(self.Fr_Gastos, bg_color="transparent", text=f"$  {self.gastos}", anchor="w", font=("Carme", 18))
        self.txt_mostrar_gastos.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)

        ###

        # LABEL DE VENTAS
        
        # Label
        self.Fr_Ventas = ctk.CTkFrame(self.Fr_Principal, fg_color="LightGrey")
        self.Fr_Ventas.place(relx=0.6, rely=0.45, relwidth=0.35, relheight=0.2)

        # Texto
        self.txt_ventas = ctk.CTkLabel(self.Fr_Ventas, bg_color="transparent", text="Ventas", anchor="w", font=("Carme", 18))
        self.txt_ventas.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)

        # Variable
        self.txt_mostrar_ventas = ctk.CTkLabel(self.Fr_Ventas, bg_color="transparent", text=f"$  {self.ventas}", anchor="w", font=("Carme", 18))
        self.txt_mostrar_ventas.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)

        ###

        # LABEL DE GANANCIAS
        
        # Label
        self.Fr_Ganancias = ctk.CTkFrame(self.Fr_Principal, fg_color="LightGrey")
        self.Fr_Ganancias.place(relx=0.6, rely=0.7, relwidth=0.35, relheight=0.2)

        # Texto
        self.txt_ganancias = ctk.CTkLabel(self.Fr_Ganancias, bg_color="transparent", text="Ganancias", anchor="w", font=("Carme", 18))
        self.txt_ganancias.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)

        # Variable
        self.txt_mostrar_ganancias = ctk.CTkLabel(self.Fr_Ganancias, bg_color="transparent", text=f"$  {self.ganancias}", anchor="w", font=("Carme", 18))
        self.txt_mostrar_ganancias.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)

        ###

        # BOTON DE EXPORTAR A EXCEL

        self.btn_exportar_excel = ctk.CTkButton(self.Fr_Principal, text="Exportar a Excel", font=("Carme", 15), command=lambda:self.obtener_gastos())
        self.btn_exportar_excel.place(relx=0.8, rely=0.05, relwidth=0.15, relheight=0.06)

    # Funcionalidad

    def obtener_gastos(self):

        self.gastos = 0

        self.bd.cursor.execute(""" SELECT subtotal FROM productos_stock """)

        self.subtotal_db = self.bd.cursor.fetchall()

        for subtotal in self.subtotal_db:

            self.gastos += subtotal[0]
        
        self.txt_mostrar_gastos.configure(text=f"$  {self.gastos}")

    def obtener_ventas(self):

        pass

    def obtener_ganancias(self):

        pass
