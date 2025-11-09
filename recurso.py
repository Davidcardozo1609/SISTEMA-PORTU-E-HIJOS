from PIL import Image
import customtkinter as ctk

class Recursos:
    """Clase que gestiona la carga y reutilización de imágenes."""
    _cache = {}

    @staticmethod
    def obtener_imagen(ruta, tamaño=None, modo_ctk=True, tamaño_visual=None):
        """
        Devuelve una imagen ya cargada o la carga solo una vez.
        - tamaño → tamaño de la imagen base (Pillow)
        - tamaño_visual → tamaño con el que se mostrará en CTkImage
        """
        clave = (ruta, tamaño, modo_ctk, tamaño_visual)
        #Guarda la info de la img
        
        
        #___SI EXISTE LA IMAGEN___#
        
        if clave in Recursos._cache:
        #si esa info existe en el diccionario(osea si esa imagen existe)
            return Recursos._cache[clave]
        #te devuelve la imagen del diccionario con esa info
        
        #___SI NO EXISTE LA IMAGEN___#
        try:
            imagen = Image.open(ruta)
            #abre la imagen
            
            if tamaño:
                imagen = imagen.resize(tamaño, Image.LANCZOS)
                #redimensiona 

            if modo_ctk:
                img_final = ctk.CTkImage(
                    light_image=imagen,
                    dark_image=imagen,
                    size=tamaño_visual or tamaño  # 👈 tamaño visible
                )
                #si existe el tamaño visual usa eso
            else:
                img_final = imagen
                #si no hay tamaño te devuelve la imagen

            Recursos._cache[clave] = img_final
            #y mete esa imagen al diccionario, para no estar abriendo una y otra vez, solo se la pasa 
            return img_final
            #y devuelve la img

        except Exception as e:
            print(f"⚠️ Error cargando imagen {ruta}: {e}")
            return None

