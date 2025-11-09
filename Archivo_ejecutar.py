from Clase_Ventana_Login import Ventana_Login
import threading #Permite ejecutar varias tareas al mismo tiempo dentro del mismo programa
from recurso import Recursos
from Constantes import *
from Clase_Gestor_Ventanas import GestorVentanas






def precargar_recursos():
    #crea una funcion que hace un diccionario y cada elemento(imagen) usa la clase recurso
    rutas = [
        LOGO_INICIO,LOGO_PERFIL,
        LOGO_BODEGA,LOGO_FACTURACION,
        LOGO_REPORTES,LOGO_CALENDARIO,
        LOGO_BD, LOGO_AJUSTES,LOGO_EXIT
    ]

    size = (50,50)
    rutas = [LOGO_INICIO, LOGO_PERFIL, LOGO_BODEGA, LOGO_FACTURACION,
             LOGO_REPORTES, LOGO_CALENDARIO, LOGO_BD, LOGO_AJUSTES, LOGO_EXIT]

    for ruta in rutas:
        Recursos.obtener_imagen(ruta, tamaño=size, modo_ctk=True, tamaño_visual=size)





if __name__ == "__main__":
    
    t = threading.Thread(target=precargar_recursos, daemon=True)
    #Este es un hilo que ejecuta una funcion mientras el programa este abierto
    t.start()
    #lo iniciaz

    
    
    app = GestorVentanas.abrir(Ventana_Login,master=None)  # raíz principalx
    
    
    app.ventana.state('zoomed')
    app.ventana.mainloop()
    









