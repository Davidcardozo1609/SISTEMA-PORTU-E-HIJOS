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
from datetime import datetime, timedelta



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
                                         text=f" 24",
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

        self.mostrar_grafico_barras()
        self.actualizar_cantidades()
        
        #_________________GRAFICO_____________________
    def mostrar_grafico_barras(self):
        hoy = datetime.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes de esta semana
        inicio_mes = hoy.replace(day=1)

        # Traer todas las ventas
        self.bd.cursor.execute("SELECT fecha, total FROM registro_ventas")
        filas = self.bd.cursor.fetchall()

        ventas_hoy = 0
        ventas_semana = 0
        ventas_mes = 0

        # Función para convertir texto a fecha
        def convertir_fecha(fecha_txt):
            try:
                # formato guardado en la BD: dd/mm/yyyy
                return datetime.strptime(fecha_txt, "%d-%m-%Y").date()

            except Exception as e:
                print("Error al convertir fecha:", fecha_txt, e)
                return None

        for fecha_txt, total in filas:
            fecha = convertir_fecha(fecha_txt)
            if not fecha:
                continue

            if fecha == hoy:
                ventas_hoy += float(total)
            if inicio_semana <= fecha <= hoy:
                ventas_semana += float(total)
            if inicio_mes <= fecha <= hoy:
                ventas_mes += float(total)


        # Preparar datos para el gráfico
        categorias = ["Hoy", "Semana", "Mes"]
        valores = [ventas_hoy, ventas_semana, ventas_mes]

        # Crear gráfico de barras
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        barras = ax.bar(categorias, valores, color=["#3B82F6", "#10B981", "#F97316"])

        # Etiquetas arriba de las barras
        for barra in barras:
            y = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2, y + 0.5, f"${y:.2f}", ha="center", va="bottom")

        ax.set_title("Ventas Totales", fontsize=14, fontweight="bold")
        ax.set_ylabel("Monto ($)")
        ax.set_xlabel("Periodo")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.Fr_Principal)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.25, rely=0.48, relwidth=0.5, relheight=0.5)


  





        
        
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

    def actualizar_cantidad_clientes(self):

        self.cntd_cli = 0

        query = """ SELECT * FROM clientes """

        self.bd.cursor.execute(query)

        clientes_detectados = self.bd.cursor.fetchall()

        for cliente in clientes_detectados:

            self.cntd_cli += 1
        
        self.Cli_Lbl_info.configure(text=f"   {self.cntd_cli}")
    
    def actualizar_cantidad_proveedores(self):

        self.cntd_prov = 0

        query = """ SELECT * FROM proveedores """

        self.bd.cursor.execute(query)

        proveedores_detectados = self.bd.cursor.fetchall()

        for cliente in proveedores_detectados:

            self.cntd_prov += 1
        
        self.prov_Lbl_info.configure(text=f"   {self.cntd_prov}")

    
    def actualizar_cantidad_categorias(self):
        try:
            self.bd.cursor.execute("SELECT COUNT(DISTINCT categoria) FROM productos_stock")
            cantidad_categorias = self.bd.cursor.fetchone()[0] or 0
            self.ctg_Lbl_info.configure(text= f"   {cantidad_categorias}")
        except:
            cantidad_categorias = 0

    def actualizar_cantidad_productos(self):
        try:
            self.bd.cursor.execute("SELECT COUNT(DISTINCT producto) FROM productos_stock")
            cantidad_productos = self.bd.cursor.fetchone()[0] or 0
            self.prod_Lbl_info.configure(text= f"   {cantidad_productos}")
        except:
            cantidad_productos = 0

    
    def actualizar_cantidades(self):

        self.actualizar_cantidad_clientes()
        self.actualizar_cantidad_proveedores()
        self.actualizar_cantidad_categorias()
        self.actualizar_cantidad_productos()
        self.mostrar_grafico_barras()
            
        
"""class Plantilla:
    def __init__(self, titulo):
    #EN SU INIT TIENE TITULO
        print(f"Plantilla creada con título: {titulo}")

class Menu(Plantilla):
    def __init__(self, titulo, usuario):
    
        super().__init__(titulo)  # le paso el parámetro que necesita Plantilla
        # le paso el parámetro que necesita Plantilla 
        print(f"Menú iniciado para {usuario}")"""
        
        
                                   

        
        

        
        
        

       

        




                    
        


