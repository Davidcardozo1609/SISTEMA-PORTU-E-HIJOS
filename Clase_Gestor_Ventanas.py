
#Esta clase fue creada con el proposito de manejar el moverse entre clases
#anteriormente utilizaba una funcion para eso pero creaba muchas instanciancias lo que
#hacia mas lento todo y menos eficiente.Es esto creado en una clase para ser mas independiente y escalable


"""Una instancia es guardar una clase en una variable y ejecutar su init
y te permite acceder a elementos de la misma"""

class GestorVentanas:
    instancias = {}  # Guarda las instancias por clase
    

    @staticmethod
    def abrir(clase, *args, **kwargs):
        # Si ya existe una instancia, simplemente la muestra
        if clase in GestorVentanas.instancias:
            ventana = GestorVentanas.instancias[clase]
            if hasattr(ventana, "ventana"):
                ventana.ventana.state('zoomed')
                ventana.ventana.deiconify()
                
            return ventana

        # Si no existe, la crea y la guarda
        nueva = clase(*args, **kwargs)
        GestorVentanas.instancias[clase] = nueva
        return nueva
    #al crear la instancia se ejecuta el init creando la ventana

    @staticmethod
    def cerrar(clase):
        # Elimina la instancia (cuando se destruye o se cierra)
        if clase in GestorVentanas.instancias:
            del GestorVentanas.instancias[clase]
            
    @staticmethod
    def obtener(clase):
        """
        Devuelve la instancia de una ventana ya creada,
        o None si no existe todavía.
        """
        return GestorVentanas.instancias.get(clase, None)
