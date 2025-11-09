#__________LIBRERIAS___________#

#Base de Datos
import sqlite3 as sqlcon

#Interfaz
import customtkinter as ctk
from tkinter import messagebox as ms
import sys, os

#Otras clases
from Constantes import *
from Archivo_Ventana_Base import VentanaBase
from bd import BaseDeDatos
from Clase_Gestor_Ventanas import GestorVentanas


#___________________________________CLASE REGISTRO______________________________________#
class Ventana_Registro(VentanaBase):
    def __init__(self, master=True):
        super().__init__(master, titulo="Registro")
        
        self.bd = BaseDeDatos()
        

        # Frame
        self.frame_principal= ctk.CTkFrame (self.ventana, fg_color = "#223B40")
        self.frame_principal.place (relx = 0, rely = 0, relwidth= 1, relheight = 1)
        
        self.crear_imagenes()
        
        self.Crear_Limitaciones()
        
        self.Crear_Labels()
        
        self.Crear_Entrys()
        
        self.Desenfocar()
        
        self.Crear_Botones()
        
        
    
        
        
        
    def Crear_Labels(self):
        
        #ICONO DEL USUARIO
        
        self.icono_usuario_lbl = ctk.CTkLabel (self.frame_principal,
                                               fg_color = "#223B40",
                                               image = self.icono_usuario_img,
                                               text=""
                                               )
        
        self.icono_usuario_lbl.place (relx = 0.338, rely = 0.05, relwidth = 0.3, relheight = 0.3)
        
        #USUARIO 
        self.label_usuario = ctk.CTkLabel(self.frame_principal,
                                   text=ph_usuario,
                                   anchor="sw",
                                   fg_color=COLOR_LABELS,
                                   text_color = "white",
                                   font=("Carme", 14))
        
        self.label_usuario.place(relx=POS_IZQ_ENTRYS, rely=0.38, relwidth=0.25, relheight=0.04)
        
        self.label_conf_usuario = ctk.CTkLabel(self.frame_principal,
                                        text=ph_confirmar_usuario,
                                        anchor="sw",
                                        fg_color=COLOR_LABELS,
                                        text_color="white",
                                        font=("Carme", 14))
        
        self.label_conf_usuario.place(relx=POS_DER_ENTRYS, rely=0.38, relwidth=0.25, relheight=0.04)
        
        #CONTRASEÑA
        self.label_contrasena = ctk.CTkLabel(self.frame_principal,
                                      text=ph_contrasena,
                                      anchor="sw",
                                      text_color="white",
                                      fg_color=COLOR_LABELS,
                                      font=("Carme", 14))
                                      
        self.label_contrasena.place(relx=POS_IZQ_ENTRYS, rely=0.48, relwidth=0.25, relheight=0.04)
        
        self.label_conf_contrasena = ctk.CTkLabel(self.frame_principal,
                                           text=ph_confirmar_contrasena,
                                           anchor="sw",
                                           text_color="white",
                                           fg_color=COLOR_LABELS,
                                           font=("Carme", 14)
                                           )
        
        self.label_conf_contrasena.place(relx=POS_DER_ENTRYS, rely=0.48, relwidth=0.25, relheight=0.04)
        
        #CORREO ELECTRONICO
        
        self.label_email = ctk.CTkLabel(self.frame_principal,
                                        text=ph_correo,
                                        anchor="sw",
                                        fg_color=COLOR_LABELS,
                                        text_color="white",
                                        font=("Carme", 14))
        
        self.label_email.place(relx=POS_IZQ_ENTRYS, rely=0.58, relwidth=0.25, relheight=0.04)
        
        
        self.label_conf_email = ctk.CTkLabel(self.frame_principal,
                                             text=ph_confirmar_correo,
                                             anchor="sw",
                                             fg_color=COLOR_LABELS,
                                             text_color="white",
                                             font=("Carme", 14))
        
        self.label_conf_email.place(relx=POS_DER_ENTRYS, rely=0.58, relwidth=0.25, relheight=0.04)
        
        #NOMBRE
        
        self.label_nombre = ctk.CTkLabel(self.frame_principal,
                                         text=ph_nombre,
                                         anchor="sw",
                                         fg_color=COLOR_LABELS,
                                         text_color = "white",
                                         font=("Carme", 14))
        
        self.label_nombre.place(relx=POS_IZQ_ENTRYS, rely=0.68, relwidth=0.25, relheight=0.04)
        
        #APELLIDO
        
        self.label_apellido = ctk.CTkLabel(self.frame_principal,
                                           text=ph_apellido,
                                           anchor="sw",
                                           fg_color=COLOR_LABELS,
                                           text_color="white",
                                           font=("Carme", 14))
        
        self.label_apellido.place(relx=POS_DER_ENTRYS, rely=0.68, relwidth=0.25, relheight=0.04)
        
        

        
    def Crear_Entrys(self):
        
        #USUARIO ENTRY
        self.entry_usuario = ctk.CTkEntry(self.frame_principal,
                                   fg_color="#858E95",
                                   font=("Carme", 16),
                                   validate="key",
                                   validatecommand=self.limitar_a_30_caracteres_y_simbolos,
                                   text_color="Black"       
                                   )
        
        self.entry_usuario.place(relx=POS_IZQ_ENTRYS, rely=0.42, relwidth=0.25, relheight=0.05)

        self.entry_conf_usuario = ctk.CTkEntry(self.frame_principal,
                                        fg_color="#858E95",
                                        font=("Carme", 16),
                                        validate="key",
                                        text_color="Black",
                                        validatecommand=self.limitar_a_30_caracteres_y_simbolos
                                        )
        
        self.entry_conf_usuario.place(relx=POS_DER_ENTRYS, rely=0.42, relwidth=0.25, relheight=0.05)
        
        #CONTRASEÑA ENTRYS
        self.entry_contrasena = ctk.CTkEntry(self.frame_principal,
                                      show="*",fg_color="#858E95",
                                      font=("Carme", 16),
                                      validate="key",
                                      text_color="Black",
                                      validatecommand=self.limitar_a_30_caracteres_y_simbolos
                                      )
        
        self.entry_contrasena.place(relx=POS_IZQ_ENTRYS, rely=0.52, relwidth=0.25, relheight=0.05)
        
        self.entry_conf_contrasena = ctk.CTkEntry(self.frame_principal,
                                           show="*",
                                           fg_color="#858E95",
                                           font=("Carme", 16),
                                           validate="key",
                                           text_color="Black",
                                           validatecommand=self.limitar_a_30_caracteres_y_simbolos
                                           )
        
        self.entry_conf_contrasena.place(relx=POS_DER_ENTRYS, rely=0.52, relwidth=0.25, relheight=0.05)
       
        #CORREO ELECTRONICO ENTRYS
        self.entry_email = ctk.CTkEntry(self.frame_principal,
                                        fg_color="#858E95",
                                        font=("Carme", 16),
                                        validate="key",
                                        text_color="Black",
                                        validatecommand=self.limitar_a_50_caracteres
                                        )
        
        self.entry_email.place(relx=POS_IZQ_ENTRYS, rely=0.62, relwidth=0.25, relheight=0.05)

        self.entry_conf_email = ctk.CTkEntry(self.frame_principal,
                                             fg_color="#858E95",
                                             font=("Carme", 16),
                                             validate="key",
                                             text_color="Black",
                                             validatecommand=self.limitar_a_50_caracteres
                                             )
        
        self.entry_conf_email.place(relx=POS_DER_ENTRYS, rely=0.62, relwidth=0.25, relheight=0.05)

        #NOMBRE ENTRYS

        self.entry_nombre = ctk.CTkEntry(self.frame_principal,
                                         fg_color="#858E95",
                                         font=("Carme", 16),
                                         validate="key",
                                         text_color="Black",
                                         validatecommand=  self.limitar_a_30_caracteres)
        
        self.entry_nombre.place(relx=POS_IZQ_ENTRYS, rely=0.72, relwidth=0.25, relheight=0.05)
        
        self.entry_nombre.bind("<FocusOut>",self.formatear_entry_nombre)

        #APELLIDO  ENTRYS
        
        self.entry_apellido = ctk.CTkEntry(self.frame_principal,
                                           fg_color="#858E95",
                                           font=("Carme", 16),
                                           validate="key",
                                           text_color="Black",
                                           validatecommand= self.limitar_a_30_caracteres)
        
        self.entry_apellido.place(relx=POS_DER_ENTRYS, rely=0.72, relwidth=0.25, relheight=0.05)
        
        self.entry_apellido.bind("<FocusOut>",self.formatear_entry_apellido)


        
      
    def Desenfocar(self):
        self.entry_usuario.bind("<Return>", lambda e: self.entry_conf_usuario.focus())
        self.entry_conf_usuario.bind("<Return>", lambda e: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", lambda e: self.entry_conf_contrasena.focus())
        self.entry_conf_contrasena.bind("<Return>", lambda e: self.entry_email.focus())
        self.entry_email.bind("<Return>", lambda e: self.entry_conf_email.focus())
        self.entry_conf_email.bind("<Return>", lambda e: self.entry_nombre.focus())
        self.entry_nombre.bind("<Return>", lambda e: self.entry_apellido.focus())
        self.entry_apellido.bind("<Return>", lambda e: self.registrarse())
        
    def Crear_Botones(self):
        
        # Boton: Registro
        self.registroboton = ctk.CTkButton(self.frame_principal,
                                           text=ph_registrarse,
                                           text_color="white",
                                           fg_color="#1e1e1e",
                                           font=("Carme", 15),
                                           command=self.registrarse
                                           )
        
        self.registroboton.place(relx=0.408, rely=0.85, relwidth=0.16, relheight=0.06)
        
        # Boton: Mostrar/Ocultar Contraseña
        self.mostrar_contra = ctk.CTkButton(self.frame_principal,
                                            image = self.icono_ojo_cerrado_img,
                                            text="",
                                            fg_color = "#858E95",
                                            hover=False,
                                            command= self.mostrarcontra
                                            )
        
        self.mostrar_contra.place (relx=0.42, rely = 0.53, relwidth = 0.022, relheight = 0.027)
        
        # Boton: Mostrar/Ocultar Confirmar Contraseña
        self.mostrar_confi = ctk.CTkButton (self.frame_principal,
                                            image = self.icono_ojo_cerrado_img,
                                            text="",
                                            fg_color = "#858E95",
                                            hover=False,
                                            command= self.mostrarconfirmacion
                                            )
        
        self.mostrar_confi.place (relx=0.72, rely=0.53, relwidth=0.022, relheight=0.027)
        
        # Boton: Flecha Atras
        self.flecha_atras = ctk.CTkButton(self.frame_principal,
                                          image = self.icono_flecha,
                                          text="",
                                          fg_color = "#223B40",
                                          hover=False,
                                          command=lambda: self.ir_a_pantalla_x(
                                              __import__("Clase_Ventana_Login").Ventana_Login,  # 👈 import diferido
                                              master=None  ))
        
        self.flecha_atras.place (relx=0.001, rely=0.02, relwidth=0.07, relheight=0.08)
        
        # Variables de Mostrar/Ocultar Contraseñas
        self.contrasenaoculta = True
        self.confioculta = True


    
    def mostrarcontra(self):
        
        if self.contrasenaoculta == True:
            self.entry_contrasena.configure(show="")
            self.mostrar_contra.configure (image = self.icono_ojo_img)
            self.contrasenaoculta = False
        else:
            self.entry_contrasena.configure(show="*")
            self.mostrar_contra.configure (image = self.icono_ojo_cerrado_img)
            self.contrasenaoculta = True

    
    def mostrarconfirmacion(self):
        
        if self.confioculta == True: #Silavariable existe (True) entrara al If, si esta noexiste (False) entrara al else, y,al estar elboton sin lambda, esta funcion estara 24/7 corriendo,haciendoqueelbotonmantengasu estado y los valores queden
            
            self.entry_conf_contrasena.configure(show= "")
            self.mostrar_confi.configure (image = self.icono_ojo_img)
            self.confioculta = False
        else:
            self.entry_conf_contrasena.configure(show="*")
            self.mostrar_confi.configure (image = self.icono_ojo_cerrado_img)
            self.confioculta = True
                                    

    def formatear_entry_nombre(self, event):
        self.formatear_entry(self.entry_nombre)
    
    def formatear_entry_apellido(self, event):
        self.formatear_entry(self.entry_apellido)

    def registrarse(self):
    
        
        valor_usuario = self.entry_usuario.get()
        print (valor_usuario)
        valor_usuario_confirmo = self.entry_conf_usuario.get()
        print (valor_usuario_confirmo)
        valor_contrasena = self.entry_contrasena.get()
        print (valor_contrasena)
        valor_contrasena_confirmo = self.entry_conf_contrasena.get()
        print (valor_contrasena_confirmo)
        valor_email = self.entry_email.get()
        print(valor_email)
        valor_email_confirmo = self.entry_conf_email.get()
        print (valor_email_confirmo)
        valor_nombre = self.entry_nombre.get()
        print (valor_nombre)
        valor_apellido = self.entry_apellido.get()
        print (valor_apellido)
        if not valor_usuario or not valor_usuario_confirmo:
            ms.showerror ("Error!", "Hay que completar las casillas de Usuarios.", parent = self.ventana)
            return

        elif valor_usuario != valor_usuario_confirmo:
            ms.showerror ("Error!", "Las casillas de Usuario no coinciden.", parent = self.ventana)
            return #es para impedir que no sigan la funcion
        query = ("""SELECT * FROM usuarios WHERE usuario = ?""")
        data = (valor_usuario,)
        self.bd.cursor.execute (query,data)
        self.er = self.bd.cursor.fetchone()
        if self.er:
            ms.showerror("Error!", "El usuario ya está registrado.",parent = self.ventana)
            return
           
        elif not valor_contrasena or not valor_contrasena_confirmo:
            ms.showerror ("Error!", "Hay que completar las casillas de Contraseñas.", parent = self.ventana)
            return
        elif valor_contrasena != valor_contrasena_confirmo:
            ms.showerror ("Error!", "Las casillas de Contraseña no coinciden.", parent = self.ventana)
            return
        elif not valor_email or not valor_email_confirmo:
            ms.showerror ("Error!", "Hay que completar las casillas de Correos Electrónicos.", parent = self.ventana)
            return
        elif valor_email != valor_email_confirmo:
            ms.showerror("Error!", "Las casillas de Correo Electrónico no coinciden.", parent=self.ventana)
            return
        elif not "@" in valor_email and not "." in valor_email: #le puse not
            ms.showerror ("Error!", "Los Correos Electrónicos requiere una dirección valida (con @ y .).", parent = self.ventana)
            return
        query = ("""SELECT * FROM usuarios WHERE correo = ?""")
        data = (valor_email,)
        self.bd.cursor.execute(query,data)
        self.comprobacion = self.bd.cursor.fetchone()
        if self.comprobacion:
            ms.showerror ("Error!", "Correo Electronico ya registrado.", parent = self.ventana)
            return
        elif not valor_nombre:
            ms.showerror("Error!","Le falta colocar su nombre.", parent = self.ventana)
            return
        elif not valor_apellido:
            ms.showerror ("Error!", "Le falta colocar su apellido.", parent = self.ventana)
            return
        elif not valor_usuario or not valor_contrasena or not valor_email or not valor_nombre or not valor_apellido \
           or not valor_usuario_confirmo or not valor_contrasena_confirmo or not valor_email_confirmo:
            ms.showerror("Error!", "Por favor compléte todos los campos.", parent=self.ventana)
            return

        else:
            
            self.bd.cursor.execute ("""

            INSERT INTO usuarios (usuario, contrasena,  correo, nombre, apellido ) VALUES (?,?,?,?,?)

            """,(valor_usuario,  valor_contrasena,  valor_email,  valor_nombre, valor_apellido))
            self.bd.conexion.commit()
            ms.showinfo ("Registrado exitosamente.", "Te has registrado exitosamente.", parent = self.ventana)
            from Clase_Ventana_Login import Ventana_Login
            Ventana_Login (master = self.ventana) #le pasas el master asi no se jode todo
            self.ventana.withdraw()  #withdraw es para sacar la ventana
            
    
        
