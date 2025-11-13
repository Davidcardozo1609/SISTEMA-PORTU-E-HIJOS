#___________LIBRERIAS_______________

#Interfaz
import tkinter as tk
import customtkinter as ctk
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import messagebox as ms

#Base de Datos
import sqlite3 as sqlcon

#Clases importadas
from bd import BaseDeDatos  
from Constantes import *
from recurso import Recursos
from Clase_Gestor_Ventanas import GestorVentanas

#Etc
import threading
import sys, os

#AVISO EN ESTA PANTALLA HAY POCAS ABREVIACIONES PERO EN LAS SIGUENTES
#SE VA A ABREVIAR MAS



#_________________CLASE DE PANTALLA PRINCIPAL_____________
class Clase_Plantilla():
    def __init__(self,master=None,titulo=None, ventana_padre=None, ventana_login=None, usuario_actual=None, parent_app=None,no_abrir_ventana=None):
        self.master = master
        self.usuario_actual = usuario_actual
        self.ventana_padre = ventana_padre
        self.ventana_login = ventana_login
        self.parent_app = parent_app
        
        if no_abrir_ventana is None:
            self.crear_ventana(titulo="Menu Principal")
        else:
            self.ventana = ctk.CTkToplevel(self.master) if self.master else ctk.CTk()
            self.ventana.title(titulo)
            self.ventana.withdraw()
        
        self.ventana.minsize(width=1200, height=650)
        
        self.configurar_estilos()
        
        self.Crear_Frames()
        
        self.bd = BaseDeDatos()
        
        self.imagenes = {}
        self.cargar_imagenes()
        self.crear_menu_costado()
        
        self.crear_botones_superiores()
        
        
        #_______________________________REGISTRO DE FUNCIONES_____________________________________
        
        
        self.limitar_a_numeros_letra = (self.ventana.register(self.limite_de_caracteres_letras_numeros), "%P")
        self.limitar_letras_espacios = (self.ventana.register(self.limite_de_caracteres_espacios_letras), "%P")
        self.limitar_numeros = (self.ventana.register(self.limite_de_caracteres_numeros), "%P")
        self.validar_decimal2 = (self.ventana.register(self.validar_decimal), "%P")
        self.validar_correo = (self.ventana.register(self.limite_de_caracteres_correo), "%P")
        
        
        
        

        

        # --- creación de ventana ---
        # Si se pasa un master, creamos un Toplevel (ventana secundaria)
        # Si no hay master, se crea una ventana principal
    def crear_ventana(self, titulo):
        self.ventana = ctk.CTkToplevel(self.master) if self.master else ctk.CTk()
        self.ventana.title(titulo)
        self.ventana.state('zoomed')


        
        
        #ESTILOS
    def configurar_estilos(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        
    def Crear_Frames(self):
            
        self.Fr_costado = ctk.CTkFrame(self.ventana, fg_color="#0d3139")
        self.Fr_costado.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        
        self.Fr_blanco = ctk.CTkFrame(self.ventana, fg_color="#d2d4d7")
        self.Fr_blanco.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        
        self.Fr_con_borde = ctk.CTkFrame(self.Fr_blanco, fg_color="#d2d4d6")  # gris MUY clarito
        self.Fr_con_borde.place(relx=0.05, rely=0.07, relwidth=0.9, relheight=0.86)

        # Frame real dentro, un poquito más chico (el "contenido")
        self.Fr_Principal = ctk.CTkFrame(self.Fr_con_borde, fg_color="#fdfdfd")
        self.Fr_Principal.place(relx=0.001, rely=0.001, relwidth=0.998, relheight=0.998)
        
    

    def crear_menu_costado(self):
        
        self.Nombre_empresa = ctk.CTkLabel(
            self.Fr_costado,
            text="Portu E Hijos S.R.L.",
            text_color="white",
            fg_color="#0d3139",
            font=("Arial", 35),
            anchor="w",
            wraplength=250,   # ancho máximo antes de saltar línea
            justify="center"
        )

        
        self.Nombre_empresa.pack(fill="x", pady=(30,20),padx=(30,15))

        self.Inicio=ctk.CTkButton(self.Fr_costado,
                                  text=" Inicio",
                                  image=self.logo_inicio_tk,
                                  compound="left",
                                  anchor="w",
                                  text_color="white",
                                  fg_color="#0d3139",
                                  font=FONT_BTNS_MENU,
                                  command=lambda: self.ir_a_pantalla_x(
                                   clase_nueva=__import__("Clase_Ventana_Pantalla_Principal").Ventana_Pantalla_Principal,
                                   master=self.ventana,
                                   ventana_padre=None,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=None))
        
        self.Inicio.pack(fill="x",padx=15,pady=5)
        
        self.crear_bodega()
        self.crear_facturacion()
        self.crear_reportes()
        
        self.Calendario_Bn= ctk.CTkButton(self.Fr_costado,
                                  text=" Calendario",
                                  fg_color="#0d3139",
                                  image=self.logo_calendario_tk,
                                  compound="left",
                                  anchor="w",
                                  text_color="white",
                                  font=FONT_BTNS_MENU,
                                  command=lambda: self.ir_a_pantalla_x(
                                   __import__("Clase_Calendario").Calendario,  # 👈 import diferido
                                   master=self.ventana,
                                   titulo="Calendario",
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=None
                                   )
                                )
        self.Calendario_Bn.pack(fill="x",padx=15,pady=5)


        self.Guardar_Bn= ctk.CTkButton(self.Fr_costado,
                                   text=" Guardar BD",
                                   fg_color="#0d3139",
                                   image=self.logo_bd_tk,
                                   compound="left",
                                   anchor="w",
                                   text_color="white",
                                   font=FONT_BTNS_MENU,
                                   command=self.bd.guardar_copia)
        
        self.Guardar_Bn.pack(fill="x",padx=15,pady=5)
        
        

        
        
        
        
        
    def crear_bodega(self):
        self.Fr_bodega= ctk.CTkFrame(self.Fr_costado, fg_color="#0d3139")
        self.Fr_bodega.pack(fill="x")
        self.Fr_bodega_help = ctk.CTkFrame(self.Fr_bodega, fg_color="#0d3139")
        self.Fr_bodega_help.pack(fill="x")
        #le puse asi ya que este frame nos ayuda en poner los label y flechas
        
        #Bodega Label
        self.Bodega_Label=ctk.CTkLabel(self.Fr_bodega_help,
                                 text="  Bodega",
                                 fg_color="#0d3139",
                                 image=self.logo_bodega_tk,
                                 compound="left",
                                 anchor="w",
                                 text_color="white",
                                 font=FONT_BTNS_MENU)
        self.Bodega_Label.pack(side="left",fill="x",expand=True,padx=25,pady=6)
        
        #Botones del despegable de Bodega
        try:
            self.flecha_despegable = ctk.CTkButton(
                self.Fr_bodega_help,
                image=self.logo_abajo_tk,
                fg_color="#0d3139",
                text="",
                command=self.despegable_bodega
            )
        except Exception as e:
            print("Error al cargar imagen de Bodega:", e)
            self.flecha_despegable = ctk.CTkButton(
                self.Fr_costado,
                text="↓",
                text_color="white",
                fg_color="#0d3139",
                font=("Arial", 12, "bold"),
                command=self.despegable_bodega
            )
            
        self.flecha_despegable.pack(side="right")
        
        self.Fr_bodega_Btns= ctk.CTkFrame(self.Fr_bodega, fg_color="#0d3139")
        #Productos
        self.Productos_Bn=ctk.CTkButton(self.Fr_bodega_Btns,
                                text=" Productos",
                                fg_color="#0d3139",
                                image=self.logo_productos_tk,
                                compound="left",
                                anchor="w",
                                text_color="white",
                                font=FONT_BTNS_DESPEGABLE,
                                command=lambda: self.ir_a_pantalla_x(
                                   __import__("Clase_Ventana_Stock").Productos,  # 👈 import diferido

                                   master=self.ventana,
                                   titulo="Productos",
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=None
                                   ))
        self.Productos_Bn.pack(fill="x",padx=30,pady=3)

        
        #Proveedores
        self.Proveedores_Bn=ctk.CTkButton(self.Fr_bodega_Btns,
                                text="Proveedores",
                                fg_color="#0d3139",
                                image=self.logo_proveedores_tk,
                                compound="left",
                                anchor="w",
                                text_color="white",
                                font=FONT_BTNS_DESPEGABLE,
                                command=lambda: self.ir_a_pantalla_x(
                                   __import__("proveedores").Proveedores,  # 👈 import diferido

                                   master=self.ventana,
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=self
                                   ))
        
        self.Proveedores_Bn.pack(fill="x",padx=30,pady=3)

        

        self.Compras_Bn=ctk.CTkButton(self.Fr_bodega_Btns,
                               text=" Compras",
                               fg_color="#0d3139",
                               image=self.logo_compras_tk,
                               compound="left",
                               anchor="w",
                               text_color="white",
                               font=FONT_BTNS_DESPEGABLE,
                               command=lambda: self.ir_a_pantalla_x(
                                   __import__("Archivo_Registro_Compras").Registro_Compras,  # 👈 import diferido

                                   master=self.ventana,
                                   ventana_padre=self,
                                   ventana_login=self.ventana_login,
                                   usuario_actual=self.usuario_actual,
                                   parent_app=self
                                    ))
        
        self.Compras_Bn.pack(fill="x",padx=30,pady=3)

    def crear_facturacion(self):

        self.Fr_facturacion= ctk.CTkFrame(self.Fr_costado, fg_color="#0d3139")
        self.Fr_facturacion.pack(fill="x")
        self.Fr_facturacion_help= ctk.CTkFrame(self.Fr_facturacion, fg_color="#0d3139")
        self.Fr_facturacion_help.pack(fill="x")
        
        
        self.Facturacion_Label=ctk.CTkLabel(self.Fr_facturacion_help,
                                 text="  Facturacion",
                                 fg_color="#0d3139",
                                 image=self.logo_facturacion_tk,
                                 compound="left",
                                 anchor="w",
                                 text_color="white",
                                 font=FONT_BTNS_MENU,
                                 )
        self.Facturacion_Label.pack(side="left",fill="x",expand=True,padx=25,pady=5)
        
        #Botones del despegable de Facturacion
        try:
            self.flecha_Facturacion = ctk.CTkButton(
                self.Fr_facturacion_help,
                image=self.logo_abajo_tk,
                fg_color="#0d3139",
                text="",
                command=self.despegable_facturacion
            )
        except Exception as e:
            print("Error al cargar imagen de Facturacion:", e)
            self.flecha_Facturacion = ctk.CTkButton(
                self.Fr_facturacion_help,
                text="↓",
                text_color="white",
                fg_color="#0d3139",
                font=("Arial", 12, "bold"),
                command=self.despegable_facturacion
            )
            
        self.flecha_Facturacion.pack(side="right")
        
        self.Fr_facturacion_Btns = ctk.CTkFrame(self.Fr_facturacion, fg_color="#0d3139")
        #Frame para los botones despegables
        
        self.Clientes_Bn = ctk.CTkButton(
            self.Fr_facturacion_Btns,
            text=" Clientes",
            fg_color="#0d3139",
            image=self.logo_clientes_tk,
            compound="left",
            anchor="w",
            text_color="white",
            font=FONT_BTNS_DESPEGABLE,
            command=lambda: self.ir_a_pantalla_x(
                __import__("Clase_Ventana_Clientes").Clientes,  # 👈 import diferido

                master=self.ventana,
                titulo="Clientes",
                ventana_padre=self,
                ventana_login=self.ventana_login,
                usuario_actual=self.usuario_actual,
                parent_app=None
                )
            )
        self.Clientes_Bn.pack(fill="x",padx=30,pady=3)
        
    

        
        self.Ventas_Bn = ctk.CTkButton(
            self.Fr_facturacion_Btns,
            text=" Ventas",
            fg_color="#0d3139",
            image=self.logo_ventas_tk,
            compound="left",
            anchor="w",
            text_color="white",
            font=FONT_BTNS_DESPEGABLE,
            command=lambda: self.ir_a_pantalla_x(
                
                __import__("Clase_Ventana_Registro_Ventas").Registro_Ventas,  # 👈 import diferido
                #Aquí no se importa Ventas al inicio, solo cuando el usuario hace clic en el botón.
                #Para ese momento, Plantilla ya está cargada y no hay conflicto.
                #Así Python puede ejecutar la herencia de Ventas(Clase_Plantilla) sin problemas.
                #en los parentesis pones el nombre del archivo y fuera la ".nombre_de_la_clase"
                
                
                master=self.ventana,
                #el master es la ventana donde se ponen las cosas, ventas debe recibir el nombre de su ventana
                ventana_padre=self,
                #el padre de la ventana , se usara para facilitar cosas
                ventana_login=self.ventana_login,
                #esto es una referencia a la ventana login
                usuario_actual=self.usuario_actual,
                #el usuario
                parent_app=self
                #esto se usara cuando manejemos padre>hija>hijo2 ahi el parent ayuda mucho
                #a volver a la ventana padre real.por que si la viniendo desde la pantalla
                #hijo2, en hija  queres ir a padre, le tenes que pasar
                #la ventana padre pero el que tiene hijo2 no sirve (en fin tengo un video explicando)
                )
            )
            
    
        self.Ventas_Bn.pack(fill="x",padx=30,pady=3)
        
        self.facturacion_visible = False
   
        


    def crear_reportes(self):
        
  
        self.Fr_Reportes= ctk.CTkFrame(self.Fr_costado, fg_color="#0d3139")
        self.Fr_Reportes.pack(fill="x")
        
        self.Fr_Reportes_help = ctk.CTkFrame(self.Fr_Reportes, fg_color="#0d3139")
        self.Fr_Reportes_help.pack(fill="x")
        
        self.Reportes_Label=ctk.CTkLabel(self.Fr_Reportes_help,
                                 text="  Reportes",
                                 fg_color="#0d3139",
                                 image=self.logo_reportes_tk,
                                 compound="left",
                                 anchor="w",
                                 text_color="white",
                                 font=FONT_BTNS_MENU,
                                 )
        self.Reportes_Label.pack(side="left",fill="x",expand=True,padx=25,pady=5)
        
        
        
        #Botones del despegable de Facturacion
        try:
            self.flecha_Reportes = ctk.CTkButton(
                self.Fr_Reportes_help,
                image=self.logo_abajo_tk,
                fg_color="#0d3139",
                text="",
                command=self.despegable_reportes
            )
        except Exception as e:
            print("Error al cargar imagen de Reportes:", e)
            self.flecha_Reportes = ctk.CTkButton(
                self.Fr_Reportes_help,
                text="↓",
                text_color="white",
                fg_color="#0d3139",
                font=("Arial", 12, "bold"),
                command=self.despegable_reportes
            )
            
        self.flecha_Reportes .pack(side="right")
        
        self.Fr_Reportes_Btns = ctk.CTkFrame(self.Fr_Reportes, fg_color="#0d3139")
        
        self.Ganancias_Bn=ctk.CTkButton(self.Fr_Reportes_Btns,
                                        text=" Ganancias",
                                        fg_color="#0d3139",
                                        image=self.logo_ganancias_tk,
                                        compound="left",
                                        anchor="w",
                                        text_color="white",
                                        font=FONT_BTNS_DESPEGABLE,
                                        command=lambda: self.ir_a_pantalla_x(
                                            __import__("Clase_Ventana_Ganancias").Ganancias,
                                            master=self.ventana,
                                            titulo="Ganancias",
                                            ventana_padre=self,
                                            ventana_login=self.ventana_login,
                                            usuario_actual=self.usuario_actual,
                                            parent_app=self)
                                            )
        self.Ganancias_Bn.pack(fill="x",padx=30,pady=3)
        
        self.reportes_visible = False
        


    def crear_botones_superiores(self):
        self.cerrar_sesion_btn=ctk.CTkButton(self.Fr_blanco,
                                         image=self.logo_exit_tk,
                                         fg_color="white",
                                         command=self.cerrar_sesion)
        
        self.cerrar_sesion_btn.place(relx=0.93,rely=0.02,relwidth=0.04,relheight=0.05)
        
        self.Lbl_nombre_modulo=ctk.CTkLabel(self.Fr_Principal,
                                            text="Menu Principal",
                                            font=("Segoe UI", 40, "bold"),
                                            text_color="#333",
                                            fg_color="white")
        
        self.Lbl_nombre_modulo.place(relx=0.075,rely=0.03,relwidth=0.382,relheight=0.1)
        
        self.bodega_visible = False
    
        
    def toggle_despegable(self, frame_btns, flecha_btn, visible_flag_attr):
        #recibe el frame de los botones ocultos, la flecha, y una variable que usaremos
        
        visible = getattr(self, visible_flag_attr)
        #obtiene el valor(ya sea true o false de ese nombre)
        
        if visible:
            frame_btns.pack_forget()
            #oculya el frame
            try:
                flecha_btn.configure(image=self.logo_abajo_tk)
            except Exception:
                flecha_btn.configure(text="▼")
        else:
            frame_btns.pack(fill="x")
            #ubica el frame(mostrandolo)
            try:
                flecha_btn.configure(image=self.logo_arriba_tk)
            except Exception:
                flecha_btn.configure(text="▲")
                
        setattr(self, visible_flag_attr, not visible)
        #cambia el valor
        
    def obtener_logos(self): 
        LOGOS = {
            "inicio": LOGO_INICIO,
            "bodega": LOGO_BODEGA,
            "productos": LOGO_PRODUCTOS,
            "ventas": LOGO_VENTAS,
            "proveedores": LOGO_PROVEEDORES,
            "compras": LOGO_COMPRAS,
            "ganancias": LOGO_GANANCIAS,
            "clientes": LOGO_CLIENTES,
            "calendario": LOGO_CALENDARIO,
            "bd": LOGO_BD,
            "ajustes": LOGO_AJUSTES,
            "facturacion": LOGO_FACTURACION,
            "descuento": LOGO_DESCUENTO,
            "categorias": LOGO_CATEGORIAS,
            "reportes": LOGO_REPORTES,
            "empresa": LOGO_EMPRESA,
            "perfil": LOGO_PERFIL,
            "exit": LOGO_EXIT,
            "campana": LOGO_CAMPANA,
            "arriba": LOGO_DESPEGABLE_ARRIBA,
            "abajo": LOGO_DESPEGABLE_ABAJO
        }

        # Opcional: imágenes de info o botones despegables
        LOGOS_INFO = {
            "clientes_info": LOGO_CLIENTES_INFO,
            "proveedores_info": LOGO_PROVEEDORES_INFO,
            "categorias_info": LOGO_CATEGORIAS_INFO,
            "productos_info": LOGO_PRODUCTOS_INFO,
            
        }
        
        return LOGOS, LOGOS_INFO
    
    def cargar_todas_imagenes(self):
        
        LOGOS, LOGOS_INFO = self.obtener_logos()
        #LOGOS Y LOGOS INFO son diccionarios y solo le estamos guardando esos valores 
        self.imagenes = {}  # diccionario para guardar todas las imágenes

        # logos normales
        for key, ruta in LOGOS.items():
            # tamaño opcional según tipo de logo
            DEFAULT_SIZE = (50, 50)
            tam = TAMAÑO_LOGO_DESPEGABLE if key not in ["inicio", "perfil","bodega",
                                                        "facturacion","calendario", "bd",
                                                        "reportes","ajustes","exit"] else DEFAULT_SIZE
            self.imagenes[key] = Recursos.obtener_imagen(ruta, tamaño=tam, modo_ctk=True, tamaño_visual=tam)


        # logos info (sin CTkImage si son solo iconos pequeños)
        for key, ruta in LOGOS_INFO.items():
            self.imagenes[key] = Recursos.obtener_imagen(ruta, tamaño=(55,55), modo_ctk=False,  tamaño_visual=(80, 80))
      
    def cargar_imagenes(self):
        self.cargar_todas_imagenes()
        self.logo_inicio_tk = self.imagenes["inicio"]
        self.logo_perfil_tk = self.imagenes["perfil"]
        self.logo_bodega_tk = self.imagenes["bodega"]
        self.logo_productos_tk = self.imagenes["productos"]
        self.logo_compras_tk = self.imagenes["compras"]
        self.logo_proveedores_tk = self.imagenes["proveedores"]
        self.logo_facturacion_tk = self.imagenes["facturacion"]
        self.logo_ventas_tk = self.imagenes["ventas"]
        self.logo_clientes_tk = self.imagenes["clientes"]
        self.logo_descuento_tk = self.imagenes["descuento"]
        self.logo_reportes_tk = self.imagenes["reportes"]
        self.logo_ganancias_tk = self.imagenes["ganancias"]
        self.logo_categorias_tk = self.imagenes["categorias"]
        self.logo_calendario_tk = self.imagenes["calendario"]
        self.logo_exit_tk = self.imagenes["exit"]
        self.logo_campana_tk = self.imagenes["campana"]
        self.logo_ajustes_tk = self.imagenes["ajustes"]
        self.logo_bd_tk = self.imagenes["bd"]
        
        
        
        
        
        self.logo_clientes_info_tk = self.imagenes["clientes_info"]
        self.logo_proveedores_info_tk = self.imagenes["proveedores_info"]
        self.logo_categorias_info_tk = self.imagenes["categorias_info"]
        self.logo_productos_info_tk = self.imagenes["productos_info"]
        
        self.logo_abajo_tk = self.imagenes["abajo"]
        self.logo_arriba_tk = self.imagenes["arriba"]
    #esta parte antes eran tres funciones...
    
    def despegable_bodega(self):
        self.toggle_despegable(self.Fr_bodega_Btns, self.flecha_despegable, "bodega_visible")
        
    def despegable_facturacion(self):
        self.toggle_despegable(self.Fr_facturacion_Btns, self.flecha_Facturacion, "facturacion_visible")
        
    def despegable_reportes(self):
        self.toggle_despegable(self.Fr_Reportes_Btns, self.flecha_Reportes, "reportes_visible")


        
    # ---------------- Imagen ----------------
    
    def colocar_imagen(self, ruta, nombre="img"):
        try:
            img_original = Image.open(ruta)
            self.imagenes[nombre] = ImageTk.PhotoImage(img_original)

            lbl = ctk.CTkLabel(self.Fr_costado, image=self.imagenes[nombre])
            lbl.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.5)
            
            # Función para redimensionar cada vez que cambia el tamaño del frame
            def redimensionar(event):
                nuevo = img_original.resize((event.width, event.height))
                self.imagenes[nombre] = ImageTk.PhotoImage(nuevo)
                lbl.configure(image=self.imagenes[nombre])

            self.Fr_costado.bind("<Configure>", redimensionar)
            
        except Exception as e:
            print(f"No se pudo colocar la imagen {ruta}: {e}")
            




    def ir_a_pantalla_x(self, clase_nueva, *args, **kwargs):
        # Evita reabrir la misma ventana actual
        if isinstance(self, clase_nueva):
            return

        if hasattr(self, "ventana"):
            self.ventana.withdraw()
            #si en nuestra clase esta el atributo ventana

        return GestorVentanas.abrir(clase_nueva, *args, **kwargs)

    
    
    #isinstance es una funcion que busca si el elemento pertenece a una clase
    #devuelve True si el objeto es una instancia de esa clase o de alguna clase que herede de ella    
        

        
    def cerrar_sesion(self):
        self.ventana.withdraw()
        
        self.ir_a_pantalla_x(
            __import__("Clase_Ventana_Login").Ventana_Login)
        
    def limite_de_caracteres_letras_numeros(self,texto):
        """Solo letras y números, máximo 30 caracteres."""
        if texto == "":
            return True
        if len(texto) > 30:
            return False
        return texto.isalnum()


    def limite_de_caracteres_espacios_letras(self,texto):
        """Solo letras y espacios, máximo 30 caracteres."""
        if texto == "":
            return True
        if len(texto) > 30:
            return False
        if "  " in texto:
            return False
    
        return all(c.isalpha() or c.isspace() for c in texto)


    def limite_de_caracteres_numeros(self,texto):
        """Solo números, máximo 30 caracteres."""
        if texto == "":
            return True  # Permite borrar todo
        if len(texto) > 12:
            return False
        return texto.isdigit()#Devuelve True si todos los caracteres de la cadena son dígitos (0-9

    def formatear_texto(self,texto):
        """Capitaliza cada palabra del texto."""
        return ' '.join(p.capitalize() for p in texto.strip().split())
    
    def formatear_entry(self, event, entry):
        """Formatea texto de un Entry, capitalizando cada palabra."""
        texto = entry.get()
        texto_formateado = self.formatear_texto(texto)
        entry.delete(0, "end")
        entry.insert(0, texto_formateado)

    
    def limite_de_caracteres_correo(self,texto):
        """Validación simple de correo, máximo 50 caracteres."""
        permitidos = set("abcdefghijklmnopqrstuvwxyz0123456789@._-")
        texto = texto.lower()
        return all(c in permitidos for c in texto) and len(texto) <= 50
    
    def validar_decimal(self,texto):
        """
        Retorna True si:
        - La cadena está vacía (permitir borrar)
        - O es un número con hasta 2 decimales
        """
        if texto == "":
            return True  # permitir borrar todo
        if len(texto) > 12:
            return False

        try:
            # Intentamos convertir a float
            float(texto)
        except ValueError:
            return False  # no es un número

        # Revisamos decimales
        if "." in texto:
            partes = texto.split(".")#el punto split sirve como separador, ahi dice que corte en el punto
            #devolviendo una lista con dos elementos, los numeros enteros y los decimales
            
            if len(partes[1]) > 2: 
                return False  # más de 2 decimales
        return True
    
 
    
    #FUNCION 
    def crear_tabla(self,master,columnas=None,datos=None,con_acciones=True,detalles=None):
        

        #Fr_Tabla
        self.Fr_del_treeview = ctk.CTkFrame(master)
        self.Fr_del_treeview.pack(fill="both", expand=True, padx=10, pady=10)

        

        # Treeview
        self.tree = ttk.Treeview(self.Fr_del_treeview, columns=columnas, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        #Estilo
        
        style = ttk.Style()
        
        style.configure("Treeview", font=("Carme", 14))
        style.configure("Treeview.Heading", font=("Carme", 14))

        # Scrollbars
        self.tree_scroll = ttk.Scrollbar(self.Fr_del_treeview, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky="ns")

        scroll_x = ttk.Scrollbar(self.Fr_del_treeview, orient="horizontal", command=self.tree.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Conectar Treeview con scrollbars
        self.tree.configure(yscrollcommand=self.tree_scroll.set, xscrollcommand=scroll_x.set)

        # Que el Treeview se expanda con el frame
        self.Fr_del_treeview.grid_rowconfigure(0, weight=1)
        self.Fr_del_treeview.grid_columnconfigure(0, weight=1)

        
        # ---------------- ENCABEZADOS ----------------
        self.columnas = list(columnas)
        
        if detalles:
            self.columnas += ["Detalles"]
            
        if con_acciones:
            self.columnas += ["Editar", "Eliminar"]
            
        
            
            
        self.tree["columns"] = self.columnas  # Asegura que el Treeview reconozca todas las columnas (incluyendo Editar y Eliminar)
            
            
        for col in self.columnas:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            if col not in ["Detalles", "Editar", "Eliminar"]:
                ancho = 120
            elif col == "ID":
                ancho = 20
            else:
                ancho = 80

            self.tree.column(col, width=ancho, anchor=tk.CENTER)

        
        
        self.datos = datos if datos is not None else []
        
        
        for fila in self.datos:
            valores = list(fila)
            # Agregar columnas extra solo si existen
            if "Editar" in self.columnas:
                valores.append("Editar")
            if "Eliminar" in self.columnas:
                valores.append("Eliminar")
            if "Detalles" in self.columnas:
                valores.append("Detalles")
            self.tree.insert("", "end", values=valores)

            
        # --- Vincular clic en una celda ---
        self.tree.bind("<Button-1>", self.on_click)
        
    def on_click(self, event):
        """Detecta clics en las columnas de acción."""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not row_id or not col:
            return

        col_index = int(col.replace("#", ""))
        col_name = self.columnas[col_index - 1]
        valores = self.tree.item(row_id, "values")

        if col_name == "Editar":
            self.editar_producto(valores, row_id)
            
        elif col_name == "Eliminar":
            self.eliminar_producto(row_id, valores)
            
        elif col_name == "Detalles":
            self.ventana_detalles(row_id)



    def eliminar_producto(self, row_id, valores):
        respuesta = ms.askyesno("Eliminar", f"¿Seguro que querés eliminar {valores[0]}?",parent=self.ventana)
        if respuesta:
            self.tree.delete(row_id)
            ms.showinfo("Eliminado", f"{valores[0]} fue eliminado.",parent=self.ventana)
            self.actualizar_total()
            
    def agregar_fila(self, fila_dict, con_acciones=True):
        """
        Inserta una fila en la tabla.
        - fila_dict: diccionario cuyas claves coinciden con las columnas base.
        - con_acciones: si True, agrega los botones 'Editar' y 'Eliminar'.
        """
        valores = [fila_dict.get(col, "") for col in self.columnas if col not in ("Editar", "Eliminar")]

        if con_acciones:
            valores += ["Editar", "Eliminar"]

        self.tree.insert("", "end", values=tuple(valores))
        
    

        
        
        
        
        
        
    def editar_producto(self, valores, fila_id):
        # Abrir la ventana de edición
        self.ventana_menu = ctk.CTkToplevel(self.ventana)
        self.ventana_menu.title("Editar Producto")
        self.ventana_menu.geometry("350x300")
        self.ventana_menu.resizable(False, False)
        self.ventana_menu.grab_set()

        # Entries precargados con los valores actuales
        
        # --- Labels y Entries ---
        #label producto
        self.label_producto=ctk.CTkLabel(self.ventana_menu, text="Producto:")
        self.label_producto.place(x=20, y=20)
        
        
        self.entry_producto = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_letras_espacios)
        self.entry_producto.place(x=140, y=20)
        self.entry_producto.insert(0, valores[1])
       
        
        #label categorias
        self.label_categorias=ctk.CTkLabel(self.ventana_menu, text="Categoría:")
        self.label_categorias.place(x=20, y=60)

        self.entry_categoria = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_letras_espacios)
        self.entry_categoria.place(x=140, y=60)
        self.entry_categoria.insert(0, valores[2])
        
        
        #label cantidad
        self.label_cantidad=ctk.CTkLabel(self.ventana_menu, text="Cantidad:")
        self.label_cantidad.place(x=20, y=100)

        self.entry_cantidad = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_numeros)
        self.entry_cantidad.place(x=140, y=100)
        self.entry_cantidad.insert(0, valores[3])
                                   
        #label precio unitario
        self.label_precio_unitario=ctk.CTkLabel(self.ventana_menu, text="Precio Unitario:")
        self.label_precio_unitario.place(x=20, y=140)

        self.entry_precio_unitario = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.validar_decimal2)
        self.entry_precio_unitario.place(x=140, y=140)
        self.entry_precio_unitario.insert(0, valores[4])
        
        self.id = valores[0]

        # Botón para guardar cambios
        self.btn_guardar = ctk.CTkButton(self.ventana_menu, text="Guardar Cambios",
                                     command=lambda: self.guardar_cambios(fila_id))
        self.btn_guardar.place(x=30, y=230)
        
        self.cancelar=ctk.CTkButton(self.ventana_menu, text="Cancelar", command=lambda:self.ventana_menu.destroy())
        self.cancelar.place(x=180, y=230)
        
    def guardar_cambios(self, fila_id):
        producto = self.entry_producto.get()
        categoria = self.entry_categoria.get()
        cantidad = self.entry_cantidad.get()
        precio_unitario = self.entry_precio_unitario.get()

        # Validaciones
        if not producto.strip():
            ms.showwarning("Atención", "Completa el campo Producto", parent=self.ventana_menu)
            return
        if not categoria.strip():
            ms.showwarning("Atención", "Completa el campo Categoría", parent=self.ventana_menu)
            return
        if not cantidad.strip():
            ms.showwarning("Atención", "Completa el campo Cantidad", parent=self.ventana_menu)
            return
        if not precio_unitario.strip():
            ms.showwarning("Atención", "Completa el campo Precio Unitario", parent=self.ventana_menu)
            return

        try:
            subtotal = float(cantidad) * float(precio_unitario)
        except ValueError:
            ms.showwarning("Atención", "Cantidad y Precio Unitario deben ser números", parent=self.ventana_menu)
            return

        # Actualizar fila en Treeview
        self.tree.item(fila_id, values=(producto, categoria, cantidad, precio_unitario, subtotal, "Editar", "Eliminar"))
       
        self.bd.cursor.execute("""
        UPDATE productos_stock 
        SET producto = ?, categoria = ?, cantidad = ?, precio_unitario = ? 
        WHERE id = ?
        """, (producto, categoria, cantidad, precio_unitario, self.id))
      
        self.bd.conexion.commit()
        

        # Actualizar total si existe
        if hasattr(self, "actualizar_total") and callable(getattr(self, "actualizar_total")):
            self.actualizar_total()

        # Cerrar ventana de edición
        self.ventana_menu.destroy()



        
    def actualizar_total(self):
        # Solo ejecutar si existe lbl_total
        if not hasattr(self, "lbl_total"):
            return  # No hay label, no hacemos nada

        total = 0
        for fila_id in self.tree.get_children():
            valores = self.tree.item(fila_id, "values")
            try:
                total += float(valores[4])  # subtotal
            except (ValueError, IndexError):
                pass

        self.lbl_total.configure(text=f"Total: ${total:.2f}")




            
        
