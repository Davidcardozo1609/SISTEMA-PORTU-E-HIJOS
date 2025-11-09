import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos  
from Plantilla import Clase_Plantilla
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox as ms

class Proveedores(Clase_Plantilla):
    def __init__(self,master,titulo="Proveedores",ventana_padre=None,ventana_login=None,usuario_actual=None,parent_app=None):
        
        
                #En el init se definen las cosas que se van a ejecutar al instanciar la clase
                #entre parentesis ponemos lo que va a recibir,etc. algunos  estan en None para que
                #al no recibir ese valor no se rompa, por ejemplo compras no hace falta que le pasa un parent
                #pero si no le paso un master se rompe."""
                        
       
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
        
        self.bd = BaseDeDatos()
        
        self.Lbl_nombre_modulo.configure(text="Proveedores")



        
        
        self.Fr_opciones = ctk.CTkFrame(self.Fr_Principal,
                            fg_color="black",
                            corner_radius=20)
        
        self.Fr_opciones.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.4)
        
        #ENTRY  PROVEEDOR 
        self.proveedores_entry = ctk.CTkEntry(self.Fr_opciones,
                                              fg_color="white",
                                              text_color="black",
                                              validate="key",
                                              validatecommand=self.limitar_letras_espacios)
        
        self.proveedores_entry.place (relx = 0.4, rely = 0.1, relheight = 0.13, relwidth = 0.5)
        
        
        #ENTRY TELEFONO
        self.telefono_entry = ctk.CTkEntry (self.Fr_opciones,
                                            fg_color="white",
                                            text_color="black",
                                            validate="key",
                                            validatecommand=self.limitar_numeros)
        
        self.telefono_entry.place (relx = 0.4, rely = 0.3, relheight = 0.13, relwidth = 0.5)
        
        #ENTRY DIRECCION
        self.direccion_entry = ctk.CTkEntry (self.Fr_opciones,
                                             fg_color="white",
                                             text_color="black",
                                             validate="key",
                                             validatecommand=self.limitar_a_numeros_letra)
        
        self.direccion_entry.place (relx = 0.4, rely = 0.5, relheight = 0.13, relwidth = 0.5)
        
        #BOTON AÑADIR PROVEEEDOR
        self.proveedor_boton = ctk.CTkButton (self.Fr_opciones,
                                              text="Guardar",
                                              corner_radius=12,
                                              width=120,
                                              fg_color="#4285F4",
                                              command = lambda: self.proveedores_datos())
        
        self.proveedor_boton.place (relx = 0.25, rely = 0.7, relheight = 0.2, relwidth = 0.5)
        
        #LABELS
        
        #LABEL PROVEEDOR
        self.proveedores_label= ctk.CTkLabel(self.Fr_opciones,
                                             font=("Segoe UI", 14),
                                             width=100,
                                             anchor="e",
                                             text_color="#555",
                                             text="Proveedores:")
        
        self.proveedores_label.place (relx = 0.05, rely = 0.1, relheight = 0.1, relwidth = 0.25)
        
        self.telefono_label= ctk.CTkLabel(self.Fr_opciones,
                                          text="Telefono:",
                                          font=("Segoe UI", 14),
                                          width=100,
                                          anchor="e",
                                          text_color="#555")
        
        self.telefono_label.place (relx = 0.05, rely = 0.3, relheight = 0.1, relwidth = 0.25)
        
        self.direccion_label= ctk.CTkLabel(self.Fr_opciones,
                                           text="Direccion:",
                                           font=("Segoe UI", 14),
                                           width=100,
                                           anchor="e",
                                           text_color="#555")
        
        self.direccion_label.place (relx = 0.05, rely = 0.5, relheight = 0.1, relwidth = 0.25)
        
        
        
        
        
        
        
    def proveedores_datos (self):
        proveedor_valor = self.proveedores_entry.get()
        
        
        telefono_valor = self.telefono_entry.get()
        
        direccion_valor = self.direccion_entry.get()
        if not proveedor_valor:
            ms.showerror("Error","Debe de colocar un proveedor", parent = self.Fr_Principal)
            return
        query = ("""SELECT * FROM proveedores WHERE nombre = ?""")
        data = (proveedor_valor,)
        self.bd.cursor.execute(query, data)
        self.nombre_proveedor = self.bd.cursor.fetchone()
        if self.nombre_proveedor:
            ms.showerror("Error","Ese proveedor ya ha sido colocado", parent = self.Fr_Principal)
            return
        
        elif not telefono_valor:
            ms.showerror("Error", "Debes de colocar el telefono del proveedor", parent = self.Fr_Principal)
            return
        
        
        query = (""" SELECT * FROM proveedores WHERE telefono = ? """)
        data = (telefono_valor,)
        self.bd.cursor.execute (query,data)
        self.telefono_proveedor= self.bd.cursor.fetchone()
        if self.telefono_proveedor:
            ms.showerror("Error","Ese numero de telefono ya ha sido registrado.", parent = self.Fr_Principal)
            return
        elif not direccion_valor:
            ms.showerror("Error", "Debes de colocar la direccion del proveedor", parent = self.Fr_Principal)
            return
        query = (""" SELECT * FROM proveedores WHERE direccion = ? """)
        data = (direccion_valor,)
        self.bd.cursor.execute (query,data)
        self.direccion_proveedor= self.bd.cursor.fetchone()
        if self.direccion_proveedor:
            ms.showerror ("Error", "Esa direccion ya existe", parent = self.Fr_Principal)
            return

        self.bd.cursor.execute  ( """

            INSERT INTO proveedores (nombre, telefono, direccion) VALUES (?,?,?)
        
            """, (proveedor_valor, telefono_valor, direccion_valor))
        self.bd.conexion.commit()
        ms.showinfo ("exito", "Has añadido un proveedor")
            
    
    
        
        
        
        
        
        