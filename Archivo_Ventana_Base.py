import tkinter as tk
from PIL import Image, ImageTk
from Constantes import *
import customtkinter as ctk
from recurso import Recursos
from Clase_Gestor_Ventanas import GestorVentanas

class VentanaBase():
    def __init__(self, master=None, titulo="Ventana Base"):
        self.master = master 
        self.ventana = ctk.CTk() if master is None else ctk.CTkToplevel(master)
        self.ventana.title(titulo)
        
        self.ventana.minsize(width=1200, height=650)
        
        self.ventana.state('zoomed')
        self.ventana.update_idletasks() 
        
        #ESTILOS
        ctk.set_appearance_mode("dark")  # o "light"
        ctk.set_default_color_theme("dark-blue")
       
        self.frame_principal = ctk.CTkFrame(self.ventana, fg_color="#223d40")
        self.frame_principal.pack(fill="both", expand=True)

        self.imagenes = {}
        




    # ---------------- Imagen ----------------
    
    def colocar_imagen(self, ruta, nombre="img"):
        try:
            img_original = Image.open(ruta)
            self.imagenes[nombre] = ImageTk.PhotoImage(img_original)

            lbl = tk.Label(self.frame_principal, image=self.imagenes[nombre])
            lbl.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.5)
            
            # Función para redimensionar cada vez que cambia el tamaño del frame
            def redimensionar(event):
                nuevo = img_original.resize((event.width, event.height))
                self.imagenes[nombre] = ImageTk.PhotoImage(nuevo)
                lbl.config(image=self.imagenes[nombre])

            self.frame_principal.bind("<Configure>", redimensionar)
            
        except Exception as e:
            print(f"No se pudo colocar la imagen {ruta}: {e}")



        # ---------------- Métodos de instancia ----------------
    def formatear_entry(self, entry):
        """Formatea texto de un Entry, capitalizando cada palabra."""
        texto = entry.get()
        texto_formateado = self.formatear_texto(texto)
        entry.delete(0, tk.END)
        entry.insert(0, texto_formateado)
        
    def ir_a_pantalla_x(self, clase_nueva, *args, **kwargs):
        # Evita reabrir la misma ventana actual
        if isinstance(self, clase_nueva):
            return

        if hasattr(self, "ventana"):
            self.ventana.withdraw()
            #si en nuestra clase esta el atributo ventana

        return GestorVentanas.abrir(clase_nueva, *args, **kwargs)


    # ---------------- Métodos estáticos (no necesitan self) ----------------
    @staticmethod
    def limite_de_caracteres_usuario(texto):
        """Solo letras y números, máximo 30 caracteres."""
        if texto == "":
            return True
        if len(texto) > 30:
            return False
        return texto.isalnum()

    @staticmethod
    def limite_de_caracteres_entry(texto):
        """Solo letras y espacios, máximo 30 caracteres."""
        if texto == "":
            return True
        if len(texto) > 30:
            return False
        return all(c.isalpha() or c.isspace() for c in texto)

    @staticmethod
    def limite_de_caracteres_correo(texto):
        """Validación simple de correo, máximo 50 caracteres."""
        permitidos = set("abcdefghijklmnopqrstuvwxyz0123456789@._-")
        texto = texto.lower()
        return all(c in permitidos for c in texto) and len(texto) <= 50

    @staticmethod
    def formatear_texto(texto):
        """Capitaliza cada palabra del texto."""
        return ' '.join(p.capitalize() for p in texto.strip().split())
    
    def maximizar(self):
        try:
            self.ventana.update_idletasks()
            self.ventana.state('zoomed')
        except Exception as e:
            print("state('zoomed') falló:", e)

        def asegurar():
            try:
                self.ventana.state('zoomed')
            except:
                pass
            # fallback geometry
            try:
                w = self.ventana.winfo_screenwidth()
                h = self.ventana.winfo_screenheight()
                self.ventana.geometry(f"{w}x{h}+0+0")
            except Exception as e:
                print("fallback geometry falló:", e)

        self.ventana.after(120, asegurar)
        
    def crear_imagenes(self):
        self.icono_usuario_img=Recursos.obtener_imagen(ICONO_USUARIO, tamaño=(250,300))
        
        self.icono_ojo_img=Recursos.obtener_imagen(IMAGEN_OJO, tamaño=(17,17))
        
        self.icono_ojo_cerrado_img=Recursos.obtener_imagen(IMAGEN_OJO_CERRADO, tamaño=(17,17))
        
        self.icono_flecha=Recursos.obtener_imagen(ICONO_FLECHA, tamaño=(80,75))
        
    def Crear_Limitaciones(self):
        self.limitar_a_30_caracteres = (self.ventana.register(self.limite_de_caracteres_entry), "%P")
        self.limitar_a_30_caracteres_y_simbolos = (self.ventana.register(self.limite_de_caracteres_usuario), "%P")
        self.limitar_a_50_caracteres = (self.ventana.register(self.limite_de_caracteres_correo), "%P")
