#___________LIBRERIAS_______________
import sqlite3 as sqlcon
import tkinter as tk
from PIL import Image, ImageTk ,  ImageDraw
from tkinter import messagebox as ms
import threading
import sys, os
import customtkinter as ctk
from Plantilla import Clase_Plantilla
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Clase_Gestor_Ventanas import GestorVentanas




#ABREVIACIONES USADAS:
#Fr=Frame
#ctg=Categorias
#rd=redondeada
#Cli=Clientes o Cliente
#prov=Proveedor
#Lbl=Label
#img=Imagen
#prod=productos

#_________________CLASE DE PANTALLA PRINCIPAL________________________

class Ventana_Pantalla_Principal(Clase_Plantilla):
    #HEREDAMOS DE PLANTILLA
    def __init__(self,master=None, titulo="Menu",ventana_padre=None,ventana_login=None, usuario_actual=None,parent_app=None):
        #EN EL INIT PONEMOS LO QUE NECESITAMOS PARA QUE SE INICIE EL SISTEMA
        #OSEA LAS COSAS DE PLANTILLA PARA QUE LAS PODAMOS USAR Y SI QUEREMOS ALGO MAS
        #POR EJEMPLO QUE SE LE DEBA PASAR UN fg_color 
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)

        #ACA PONEMOS QUE HEREDAMOS EL INIT DE PLANTILLA ENTRE PARENTESIS
        #LAS COSAS QUE NECESITA PLANTILLA
        #AL FINAL HAY UN EJEMPLO COMENTADO
        self.ventana_padre = ventana_padre
        self.ventana_login = ventana_login
        self.usuario_actual = usuario_actual
        self.parent_app = parent_app


        
        ctk.set_appearance_mode("light")      # modo claro
        ctk.set_default_color_theme("blue")   # color principal por defecto
        
        
        #INSTANCIA DE STOCK
        
        Instancia_Productos = GestorVentanas.abrir(__import__("Clase_Ventana_Stock").Productos,  # 👈 import diferido
                                                   master=self.ventana,
                                                   titulo="Productos",
                                                   ventana_padre=self,
                                                   ventana_login=self.ventana_login,
                                                   usuario_actual=self.usuario_actual,
                                                   parent_app=None,
                                                   no_abrir_ventana=True
                                                   )
        
      
        
        
        #INSTANCIA DE REGISTRO_COMPRAS
        
        Instancia_Reg_Compras = GestorVentanas.abrir(__import__("Archivo_Registro_Compras").Registro_Compras,  # 👈 import diferido
                                                   master=self.ventana,
                                                   titulo="Productos",
                                                   ventana_padre=self,
                                                   ventana_login=self.ventana_login,
                                                   usuario_actual=self.usuario_actual,
                                                   parent_app=None,
                                                   no_abrir_ventana=True
                                                   )
        
        
        

        
        
        #IMAGENES
        
        # clientes
        self.img_rd_Cli = self.redondear_suave(self.logo_clientes_info_tk, radio=15)
        self.logo_Cli_info_Rd = ctk.CTkImage(light_image=self.img_rd_Cli, dark_image=self.img_rd_Cli,size=(80, 70))

        # proveedores
        self.img_rd_prov = self.redondear_suave(self.logo_proveedores_info_tk, radio=15)
        self.logo_prov_info_Rd = ctk.CTkImage(light_image=self.img_rd_prov, dark_image=self.img_rd_prov,size=(80, 70))

        # categorias
        self.img_rd_ctg = self.redondear_suave(self.logo_categorias_info_tk, radio=15)
        self.logo_ctg_info_Rd = ctk.CTkImage(light_image=self.img_rd_ctg, dark_image=self.img_rd_ctg,size=(80, 70))

        # productos
        self.img_rd_prod = self.redondear_suave(self.logo_productos_info_tk, radio=15)
        self.logo_prod_info_Rd = ctk.CTkImage(light_image=self.img_rd_prod, dark_image=self.img_rd_prod,size=(80, 70))

        
        #_______FRAMES DE AYUDA, (PERMITEN HACER EL BORDE GRIS)____________
        
        #Fr_Clientes
        self.Fr_Cli_info_help = ctk.CTkFrame(self.Fr_Principal,
                                                     corner_radius=15,
                                                     fg_color="#eaeaea")
        self.Fr_Cli_info_help.place(relx=0.075, rely=0.2, relwidth=0.2, relheight=0.2)
        
        #Fr_proveedores
        self.Fr_prov_info_help = ctk.CTkFrame(self.Fr_Principal,
                                                     corner_radius=15,
                                                     fg_color="#eaeaea")
        self.Fr_prov_info_help.place(relx=0.3, rely=0.2, relwidth=0.2, relheight=0.2)
        
        #Fr_categorias
        self.Fr_ctg_info_help = ctk.CTkFrame(self.Fr_Principal,
                                                     corner_radius=15,
                                                     fg_color="#eaeaea")
        self.Fr_ctg_info_help.place(relx=0.525, rely=0.2, relwidth=0.2, relheight=0.2)
        
        #Fr_productos
        self.Fr_prod_info_help = ctk.CTkFrame(self.Fr_Principal,
                                                     corner_radius=15,
                                                     fg_color="#eaeaea")
        self.Fr_prod_info_help.place(relx=0.75, rely=0.2, relwidth=0.2, relheight=0.2)
        
        
        #__________________FRAMES DE LOS LABELS INFO(ESTAN DENTRO DE LOS FRAME DE AYUDA)______
        self.Fr_Cli_info = ctk.CTkFrame(self.Fr_Cli_info_help,
                                                corner_radius=15,
                                                fg_color="#ffffff"
                                                )
        self.Fr_Cli_info.place(relx=0.004, rely=0.005, relwidth=0.992, relheight=0.99)
        
        self.Fr_prov_info = ctk.CTkFrame(self.Fr_prov_info_help,
                                                corner_radius=15,
                                                fg_color="#ffffff"
                                                )
        self.Fr_prov_info.place(relx=0.004, rely=0.005, relwidth=0.992, relheight=0.99)
        
        self.Fr_ctg_info = ctk.CTkFrame(self.Fr_ctg_info_help,
                                                corner_radius=15,
                                                fg_color="#ffffff"
                                                )
        self.Fr_ctg_info.place(relx=0.004, rely=0.005, relwidth=0.992, relheight=0.99)
        
        self.Fr_prod_info = ctk.CTkFrame(self.Fr_prod_info_help,
                                                corner_radius=15,
                                                fg_color="#ffffff"
                                                )
        self.Fr_prod_info.place(relx=0.004, rely=0.005, relwidth=0.992, relheight=0.99)
        
        #_________________LABELS INFO_____________________
        
        #CLIENTES
        
        #imagen/texto
        self.Cli_Lbl_info = ctk.CTkLabel(self.Fr_Cli_info,
                                         image=self.logo_Cli_info_Rd,
                                         compound="left",
                                         text="  24",
                                         font=("Arial", 24),
                                         fg_color="white",
                                         text_color="black")
        self.Cli_Lbl_info.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        
        #texto abajo
        self.Cli_Text_info= ctk.CTkLabel(self.Fr_Cli_info,
                                   text="Clientes",
                                   font=("Arial", 20),
                                   fg_color="white",
                                   text_color="black")
        self.Cli_Text_info.place(relx=0,rely=0.7,relwidth=1,relheight=0.3)
        
        
        #PROVEEDORES
        self.prov_Lbl_info = ctk.CTkLabel(self.Fr_prov_info,
                                   image=self.logo_prov_info_Rd,
                                   compound="left",
                                   text="  24",
                                   font=("Arial", 24),
                                   fg_color="white",
                                   text_color="black")
        self.prov_Lbl_info.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        
        #texto abajo
        self.prov_Text_info= ctk.CTkLabel(self.Fr_prov_info,
                                   text="Proveedores",
                                   font=("Arial", 20),
                                   fg_color="white",
                                   text_color="black")
        self.prov_Text_info.place(relx=0,rely=0.7,relwidth=1,relheight=0.3)
        
        #CATEGORIAS
        self.ctg_Lbl_info = ctk.CTkLabel(self.Fr_ctg_info,
                                   image=self.logo_ctg_info_Rd,
                                   compound="left",
                                   text="  24",
                                   font=("Arial", 24),
                                   fg_color="white",
                                   text_color="black")
        self.ctg_Lbl_info.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        
        #texto abajo
        self.ctg_Text_info= ctk.CTkLabel(self.Fr_ctg_info,
                                   text="Categorias",
                                   font=("Arial", 20),
                                   fg_color="white",
                                   text_color="black")
        self.ctg_Text_info.place(relx=0,rely=0.7,relwidth=1,relheight=0.3)
        
        #PRODUCTOS
        self.prod_Lbl_info = ctk.CTkLabel(self.Fr_prod_info,
                                   image=self.logo_prod_info_Rd,
                                   compound="left",
                                   text="  24",
                                   font=("Arial", 24),
                                   fg_color="white",
                                   text_color="black")
        self.prod_Lbl_info.place(relx=0,rely=0,relwidth=1,relheight=0.7)
        
        #texto abajo
        self.prod_Text_info= ctk.CTkLabel(self.Fr_prod_info,
                                   text="Productos",
                                   font=("Arial", 20),
                                   fg_color="white",
                                   text_color="black")
        self.prod_Text_info.place(relx=0,rely=0.7,relwidth=1,relheight=0.3)
        
        #_________________GRAFICO_____________________
        
        # Datos de ejemplo (categorías y valores)
        self.categorias = ["Ropa interior", "Pijamas", "Medias", "Otros"]
        self.valores = [120, 80, 60, 90]
        
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
        """plt.subplots() crea una figura (fig) y un eje (ax).

        figsize=(4,4) → tamaño del gráfico en pulgadas (4x4).

        dpi=100 → resolución (puntos por pulgada).

        ax es donde realmente se dibuja el gráfico."""
        
        # Crear el gráfico circular
        ax.pie(self.valores, labels=self.categorias, autopct="%1.1f%%", startangle=90)

        """ax.pie() dibuja el gráfico circular 

        valores → determina cuánto ocupa cada parte.

        labels=categorias → pone el nombre de cada porción.

        autopct="%1.1f%%" → agrega los porcentajes con 1 decimal (23.5%).

        startangle=90 → rota el gráfico para que arranque desde arriba."""

        ax.set_title("Stock por categoría")
        # Pone el título arriba del gráfico.
        
        # Integrar matplotlib en Tkinter
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.Fr_Principal)
        #convierte la figura fig de matplotlib en un widget de Tkinter dentro de la ventana .
        self.canvas_grafico.draw()
        #canvas.draw() → dibuja el gráfico en memoria.
        self.canvas_grafico.get_tk_widget()
        self.canvas_grafico.get_tk_widget().place(relx=0.25,rely=0.5,relwidth=0.5,relheight=0.5)
        #coloca el gráfico en la ventana 





        
        
    def redondear_suave(self,imagen, radio, scale=4):
        #la funcion debe recibir una imagen,radio y escala
        #esa escala en 4 esta bien es solo para agrandar la imagen
        
        W, H = imagen.size
        #consigue el ancho y alto de la imagen 
        
        big_mask = Image.new("L", (W*scale, H*scale), 0)
        #crea una "mascara",L(en grises y negros) y con el tamaño x4
        #eso para que a la hora de cortar el borde sea mas suave
        #no es lo mismo recortar el borde de una imagen de 20x20 que de 1200x800
        #el segundo queda mas suave
        
        draw = ImageDraw.Draw(big_mask)
        #hace un pincel para dibujar formas(se usara para recortar)
        
        draw.rounded_rectangle((0,0,W*scale,H*scale), radius=radio*scale, fill=255)
        #Dibuja un rectángulo con esquinas redondeadas que cubre toda la máscara
        #adentro blanco lo demas sigue negro
        
        mask = big_mask.resize((W,H), Image.LANCZOS)
        #Ahora achica esa máscara grande al tamaño real de la imagen (W×H).
        #Image.LANCZOS es un filtro de alta calidad que suaviza los bordes al reducir.
        
        img = imagen.convert("RGBA")
        #Convierte la imagen original a modo RGBA
        
        img.putalpha(mask)
        #Inserta la máscara como canal alfa (transparencia) de la imagen.
        #Donde la máscara es blanca (255) → la imagen se ve.
        #Donde es negra (0) → la imagen se vuelve transparente.
        
        return img
        #devuelve la imagen
            
        
"""class Plantilla:
    def __init__(self, titulo):
    #EN SU INIT TIENE TITULO
        print(f"Plantilla creada con título: {titulo}")

class Menu(Plantilla):
    def __init__(self, titulo, usuario):
    
        super().__init__(titulo)  # le paso el parámetro que necesita Plantilla
        # le paso el parámetro que necesita Plantilla 
        print(f"Menú iniciado para {usuario}")"""
        
        
                                   

        
        

        
        
        

       

        




                    
        


