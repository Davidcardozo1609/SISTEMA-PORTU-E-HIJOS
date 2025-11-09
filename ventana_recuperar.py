
#LIBRERIAS

from Archivo_Ventana_Base import VentanaBase
import customtkinter as ctk
from bd import BaseDeDatos
import sqlite3
from tkinter import messagebox as ms
from Clase_Gestor_Ventanas import GestorVentanas
from tkinter import *


class Clase_Ventana_Recuperar(VentanaBase):
    def __init__(self, master=True):
        super().__init__(master, titulo="Recuperar Contraseña")
        
  
        
        self.bd = BaseDeDatos()
        
        self.crear_imagenes()
        
        self.Crear_Limitaciones()
        
        
        self.frame_principal.configure(fg_color = "#223B40")

        #______ENTRYS_____#

        #Gmail para recuperar contraseña
        self.Entry_gmail = ctk.CTkEntry (self.ventana,
                                         fg_color = "#858E95",
                                         font=("Carme", 14),
                                         validate="key",
                                         validatecommand=self.limitar_a_50_caracteres,
                                         text_color="Black"
                                         )
        
        self.Entry_gmail.place (relx = 0.35, rely = 0.5, relheight = 0.05, relwidth = 0.33)
        
        #______BOTONES_____#
        
        #Boton Recuperar Contraseña
        self.recubot = ctk.CTkButton (self.ventana,
                                      text = "recuperar contraseña",
                                      fg_color = "#1A1C19",
                                      text_color = "white",
                                      font = ("Carme", 14),
                                      command = lambda: self.recuperar_fin())
        
        self.recubot.place (relx = 0.4, rely = 0.7, relheight = 0.07, relwidth = 0.2)
        
        #Boton de flecha atras
        self.flecha_atras = ctk.CTkButton(self.frame_principal,
                                          image = self.icono_flecha,
                                          fg_color = "#223B40" ,
                                          command = lambda: self.salir_flecha(),
                                          text="",
                                          hover=False)
        
        self.flecha_atras.place (relx = 0.001, rely = 0.02, relwidth = 0.1, relheight = 0.1)
        
        #______LABELS_____#
        
        #Logo del usuario
        self.icono_usuario = ctk.CTkLabel (self.frame_principal,
                                           fg_color = "#223B40",
                                           image = self.icono_usuario_img,
                                           text=""
                                           )
        
        self.icono_usuario.place (relx = 0.35, rely = 0.1, relwidth = 0.3, relheight = 0.3)
        
        #Label gmail
        self.correo = ctk.CTkLabel (self.ventana,
                                    text = "Correo Electronico",
                                    fg_color = "#223B40",
                                    text_color = "white",
                                    font = ("Carme", 14))
        
        self.correo.place (relx= 0.345, rely = 0.46, relheight = 0.04, relwidth = 0.13)
        
        #Label usuario
        self.usuariolabel = ctk.CTkLabel (self.ventana,
                                          text = "Usuario",
                                          fg_color = "#223B40",
                                          text_color = "white",
                                          font = ("Carme", 14))
        
        self.usuariolabel.place (relx = 0.31, rely = 0.56, relheight = 0.05, relwidth = 0.13)
        
        #Label contra
        self.contralabel = ctk.CTkLabel (self.ventana,
                                         text = "Contraseña",
                                         fg_color = "#223B40",
                                         text_color = "white",
                                         font = ("Carme", 14))
        
        self.contralabel.place (relx = 0.5, rely = 0.56, relheight = 0.05, relwidth = 0.13)
        

        #______LABELS DE RECUPERACION_____#
        
        #Label de recuperar contraseña
        self.contrasena = ctk.CTkLabel (self.ventana,
                                        text = "",
                                        fg_color = "#858E95",
                                        font=("Carme", 14),
                                        text_color="black")
        
        self.contrasena.place (relx=0.53, rely = 0.6, relheight = 0.05, relwidth = 0.15)
        
        #Label de recuperar usuario
        self.usuarioo = ctk.CTkLabel (self.ventana,
                                      text = "",
                                      fg_color = "#858E95",
                                      font=("Carme", 14),
                                      text_color="black")
        
        self.usuarioo.place (relx=0.35, rely = 0.6, relheight = 0.05, relwidth = 0.15)
        
        
        #________FOCUS______#
        self.Entry_gmail.bind ("<Return>",lambda e: self.recubot.focus())
        self.recubot.bind ("<Return>",lambda e: self.recuperar_fin())
        
       
    def recuperar_fin(self):
            usuario_coloco = self.Entry_gmail.get()
            print (usuario_coloco)
            query = ("""SELECT contrasena FROM usuarios WHERE correo = ?""")
            data = (usuario_coloco,)
            self.bd.cursor.execute(query,data)
            self.anali = self.bd.cursor.fetchone()
            query = ("""SELECT usuario FROM usuarios WHERE correo = ? """)
            data = (usuario_coloco,)
            self.bd.cursor.execute(query, data)
            self.anali2 = self.bd.cursor.fetchone()
            if self.anali:
                print (self.anali)
                ms.showinfo("Exito", "Aqui tienes tu usuario y contraseña",parent=self.ventana)
                self.contrasena.configure (text = self.anali)
                self.usuarioo.configure (text = self.anali2)
            elif not usuario_coloco:
                ms.showerror("Fallo", "No has colocado nada en correo",parent=self.ventana)
            else:
                ms.showerror("Fallo", "Ese correo no esta registrado o esta mal escrito",parent=self.ventana)
                
    def salir_flecha(self):
        self.Entry_gmail.delete(0,"end")
        self.usuarioo.configure(text="")
        self.contrasena.configure(text="")
        
        self.ventana.withdraw()
         
        from Clase_Ventana_Login import Ventana_Login
        GestorVentanas.abrir(Ventana_Login)
        
        
         
         
         
           
         
         

               
            
                
            
