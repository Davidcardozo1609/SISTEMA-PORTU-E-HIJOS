
#LIBRERIAS
from tkinter import *                          # Para crear ventanas, frames, labels, entry, botones, etc.
from tkinter import messagebox as ms           # Para mostrar alertas, errores e información
from PIL import Image, ImageTk                 # Para cargar y mostrar imágenes en Tkinter
import os                                      # Para manejar rutas de archivos (os.path.exists, os.path.join)
import sys                                     # Para verificar si está corriendo como ejecutable (sys._MEIPASS)
from bd import BaseDeDatos                     # Para manejar la base de datos SQLite
from Archivo_Ventana_Base import VentanaBase   # Clase base de tu ventana (herencia)
from Constantes import *                       # Para variables como IMAGEN_LOGO, IMAGEN_CONTRA, ph_usuario, etc.
import customtkinter as ctk
from Clase_Gestor_Ventanas import GestorVentanas

#VENTANA DE LOGIN

class Ventana_Login(VentanaBase):
    
    def __init__(self, master=None):
        # En este caso el master=none significa que sera la clase principal
        
        super().__init__(master, titulo="Login")
        # Hereda algunas cosas de VentanaBase (que seria como la "plantilla")
        
        self.bd = BaseDeDatos()
        # Establece la conexion con la base de datos
        

        # Establece el tamaño minimo de la ventana
        self.maximizar()

        
        # IMAGENES PARA LA PANTALLA
        self.crear_imagenes()

        # REGISTRO DE LAS FUNCIONES
        self.Crear_Limitaciones()
        

        # Frame del color de fondo
        self.frame_principal.configure(fg_color="#223b40")
        self.frame_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        # LABELS Y ENTRYS
        
        # --- USUARIO --- #
        
        # Usuario: Place Holder
        self.Usuario_texto = ctk.CTkLabel(self.frame_principal,
                                          text=ph_usuario,
                                          text_color="white",
                                          fg_color="#223b40",
                                          anchor="sw",
                                          font=("Carme", 14))
        
        self.Usuario_texto.place(relx=0.32, rely=0.5, relwidth=0.125, relheight=0.04)

        # Usuario: Entry
        self.Usuario = ctk.CTkEntry(self.frame_principal,
                             font=("Carme", 14),
                             fg_color="darkgrey",
                             validate="key",
                             validatecommand=self.limitar_a_30_caracteres_y_simbolos,
                             text_color="Black"       
                                    )
        
        self.Usuario.place(relx=0.32, rely=0.54, relwidth=0.36, relheight=0.05)
        
        # --- CONTRASEÑA --- #
        
        # Contraseña: Place Holder
        self.contrasena_texto = ctk.CTkLabel(self.frame_principal,
                                             text=ph_contrasena,
                                             text_color="white",
                                             fg_color="#223b40",
                                             anchor="sw",
                                             font=("Carme", 14))
        
        self.contrasena_texto.place(relx=0.32, rely=0.6, relwidth=0.08, relheight=0.04)
        
        # Contrasena: Entry
        self.contrasena = ctk.CTkEntry(self.frame_principal,
                                       font=("Carme", 14),
                                       fg_color="darkgrey",
                                       validate="key",
                                       text_color="Black",
                                       validatecommand=self.limitar_a_30_caracteres_y_simbolos,
                                       show="*")
        
        self.contrasena.place(relx=0.32, rely=0.64, relwidth=0.36, relheight=0.05)
        
        # BOTONES LOGIN
        
        # Botón: Iniciar sesión
        self.Iniciar1 = ctk.CTkButton(self.frame_principal,
                               text=ph_iniciar_sesion,
                               text_color="white",
                               fg_color="#1e1e1e",
                               font=("Carme", 15),
                               command=self.iniciar_sesion)
        self.Iniciar1.place(relx=0.33, rely=0.72, relwidth=0.16, relheight=0.06)

        # Botón: Registrarse
        self.Registrarse = ctk.CTkButton(self.frame_principal,
                                         text=ph_registrarse,
                                         text_color="white",
                                         fg_color="#1e1e1e",
                                         font=("Carme", 15),
                                         command=lambda: self.ir_a_pantalla_x(
                                              __import__("Clase_Ventana_Registro").Ventana_Registro,  # 👈 import diferido
                                              master=self.ventana ))
        self.Registrarse.place(relx=0.51, rely=0.72, relwidth=0.16, relheight=0.06) 
        
        # Botón: Olvidé la contraseña
        self.RecordarContraseña = ctk.CTkButton(self.frame_principal,
                                                text=ph_recordar_contra,
                                                text_color="white",
                                                fg_color="#223b40",
                                                font=("Carme", 15),
                                                command=lambda: self.ir_a_pantalla_x(
                                                    __import__("ventana_recuperar").Clase_Ventana_Recuperar,  # 👈 import diferido
                                                    master=self.ventana  ))
        
        self.RecordarContraseña.place(relx=0.42, rely=0.82, relwidth=0.16, relheight=0.06)

        # El ojo para mostrar la contraseña
        self.boton_mostrar_contrasena = ctk.CTkButton(self.frame_principal,
                                                      image=self.icono_ojo_cerrado_img if self.icono_ojo_cerrado_img else None,  # si no se cargó, deja None
                                                      command=self.mostrar_contrasena,
                                                      fg_color="darkgrey",
                                                      text="",
                                                      hover=False)
        
        self.boton_mostrar_contrasena.place(relx=0.65, rely=0.65, relwidth=0.023, relheight=0.03)
        
        # LABELS PARA LAS IMAGENES
        
        # Label: Logo (Persona)
        
        self.logo_epico = ctk.CTkLabel(self.frame_principal, image=self.icono_usuario_img,text="")
        self.logo_epico.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.3)
        
 
        # Redireccionar foco al presionar "Enter"
 
        self.Usuario.bind("<Return>", lambda e: self.contrasena.focus())
        self.contrasena.bind("<Return>", lambda e: self.iniciar_sesion())
        


# ---------- FUNCIONES ---------- #



                      
    def recurso_relativo(self,ruta):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, ruta)
        return os.path.join(os.path.abspath("."), ruta)
        
    def iniciar_sesion(self):
        
        
        global usuario_actual  # Indicamos que vamos a modificar la variable global
        
        user = self.Usuario.get().strip()
        passwd = self.contrasena.get().strip()
        
        if user and not passwd:
            
            ms.showerror("Error!", f"El casillero de {ph_contrasena} no puede estar vacio.",arent=self.ventana)
            
        if not user and passwd:
            
            ms.showerror("Error!", f"El casillero de {ph_usuario} no puede estar vacio.",parent=self.ventana)

        if not user and not passwd:
            
            ms.showerror("Error!", "Ninguno de los casilleros no puede estar vacio.",parent=self.ventana)
            
        if user and passwd: # Si ninguno de los casilleron esta vacios.
            
            # Verifica si hay algun usuario registrado

            self.bd.cursor.execute(""" SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ? """, (user, passwd))

            usuario_login = self.bd.cursor.fetchone()

            # Si se encontró algun usuario

            if not usuario_login:
                
                ms.showerror("Error!", "Datos incorrectos o usuario no registrado.",parent=self.ventana)
            
            if usuario_login:
                

                usuario_actual = usuario_login[1]  # guardo el usuario globalmente
                
                self.Usuario.delete(0, END)
                self.contrasena.delete(0, END)
                
                self.ir_a_menu()

                

                # Después de iniciar sesión correctamente
                
                
                
                
                

            
    def mostrar_contrasena(self):
        # Invierte el estado de la contraseña
        self.estado_contrasena = not getattr(self, "estado_contrasena", False)
        
        if self.estado_contrasena:
            # Mostrar contraseña
            self.contrasena.configure(show="")
            # Cambiar icono a ojo abierto (o cerrado, según tus imágenes)
            if self.icono_ojo_cerrado_img:
                self.boton_mostrar_contrasena.configure(image=self.icono_ojo_cerrado_img)
                self.boton_mostrar_contrasena.image = self.icono_ojo_cerrado_img
        else:
            # Ocultar contraseña
            self.contrasena.configure(show="*")
            # Cambiar icono a ojo cerrado (o abierto, según tus imágenes)
            if self.icono_ojo_img:
                self.boton_mostrar_contrasena.configure(image=self.icono_ojo_img)
                self.boton_mostrar_contrasena.image = self.icono_ojo_img

    
        

        
    def ir_a_menu(self):
        
        self.ventana.withdraw()  # oculta la ventana de login
        
        self.ir_a_pantalla_x(
            __import__("Clase_Ventana_Pantalla_Principal").Ventana_Pantalla_Principal,  # 👈 import diferido
            
            master=self.ventana, 
            usuario_actual=usuario_actual,
            ventana_login=self  # <-- agregamos esta referencia
        )
        
