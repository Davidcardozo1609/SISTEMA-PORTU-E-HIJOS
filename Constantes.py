#______LIBRERIAS_______#

#Interfaz
from PIL import Image, ImageTk
import sys, os


#Funcion Obtener la ruta exacta de los archivos
def obtener_ruta_absoluta(nombre_archivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    #Si estás en un .exe, construye la ruta correcta dentro de la carpeta temporal donde PyInstaller extrajo todo
    return os.path.join(os.path.abspath("."), nombre_archivo)
    #Si NO estás en un .exe, arma la ruta absoluta normal del proyecto.






#IMAGENES DE LOGIN 
ICONO_FLECHA = obtener_ruta_absoluta("flecha.png")
IMAGEN_PANTALLA_PRINCIPAL = obtener_ruta_absoluta("PANTALLA PRINCIPAL.jpeg")
IMAGEN_MOSTRAR_CONTRA = obtener_ruta_absoluta("imagen_mostrar_contra.jfif")
IMAGEN_CONTRA = obtener_ruta_absoluta("imagen_contra.jfif")


#______________________________LOGOS______________________________#
#Iniciar_sesion
IMAGEN_LOGO = obtener_ruta_absoluta("logo.png")

#______________________LOGOS_MENU________________________#


LOGO_INICIO = obtener_ruta_absoluta("logo_inicio.png")


LOGO_BODEGA = obtener_ruta_absoluta("logo_productos.png")
LOGO_PRODUCTOS = obtener_ruta_absoluta("logo_productos.png")
LOGO_VENTAS = obtener_ruta_absoluta("logo_ventas.png")
LOGO_PROVEEDORES = obtener_ruta_absoluta("logo_proveedores.png")
LOGO_COMPRAS = obtener_ruta_absoluta("logo_compras.png")
LOGO_GANANCIAS = obtener_ruta_absoluta("logo_ganancias.png")
LOGO_CLIENTES = obtener_ruta_absoluta("logo_clientes.png")
LOGO_CALENDARIO = obtener_ruta_absoluta("logo_calendario.png")
LOGO_BD = obtener_ruta_absoluta("logo_bd.png")
LOGO_AJUSTES = obtener_ruta_absoluta("logo_ajustes.png")
LOGO_EMPRESA = obtener_ruta_absoluta("logo_empresa.png")
LOGO_DESCUENTO = obtener_ruta_absoluta("logo_descuento.png")
LOGO_CATEGORIAS = obtener_ruta_absoluta("logo_categorias.png")
LOGO_FACTURACION = obtener_ruta_absoluta("logo_Facturacion.png")
LOGO_REPORTES = obtener_ruta_absoluta("logo_reportes.png")


#LABEL MENU
LOGO_CLIENTES_INFO = obtener_ruta_absoluta("logo_clientes_info.png")
LOGO_PROVEEDORES_INFO = obtener_ruta_absoluta("logo_proveedores_info.png")
LOGO_CATEGORIAS_INFO = obtener_ruta_absoluta("logo_categorias_info.png")
LOGO_PRODUCTOS_INFO = obtener_ruta_absoluta("logo_productos_info.png")


#Logos de la parte de arriba
LOGO_PERFIL = obtener_ruta_absoluta("logo_perfil.png")
LOGO_EXIT = obtener_ruta_absoluta("logo_exit.png")
LOGO_CAMPANA = obtener_ruta_absoluta("logo_campana.png")


#Logos con funciones en especifico
LOGO_DESPEGABLE_ABAJO = obtener_ruta_absoluta("logo_abajo_bodega.png") 
LOGO_DESPEGABLE_ARRIBA = obtener_ruta_absoluta("logo_arriba_bodega.png")

#______________________IMAGENES_REGISTRO________________________#

#imagen del ojo
IMAGEN_OJO = obtener_ruta_absoluta("ojo.png")

#imagen del ojo cerrado
IMAGEN_OJO_CERRADO = obtener_ruta_absoluta("ojo_cerrado.png")

#Icono Usuario
ICONO_USUARIO = obtener_ruta_absoluta("icono_usuario.png")

#Icono flecha
ICONO_FLECHA = obtener_ruta_absoluta("flecha.png")


#________________CONSTANTES_______________#}


#________CONSTANTES DE MENU____________#
CONSTANTE_TAMAÑO_LOGO=(50, 50)

TAMAÑO_LOGO_DESPEGABLE=(35, 35)



TAMAÑO_LABEL_LOGO = {"relwidth": 0.175, "relheight": 0.06}

TAMAÑO_LABEL_DESPEGABLE = {"relwidth": 0.175, "relheight": 0.15}

TAMAÑO_BOTONES_MENU = {"relwidth": 0.7, "relheight": 0.055}

FONT_BTNS_MENU= ("Arial",20)

FONT_BTNS_DESPEGABLE= ("Arial",15)


#______CONSTANTES DE REGISTRO_______#
COLOR_LABELS = "#223b40"

POS_IZQ_ENTRYS = 0.2
POS_DER_ENTRYS = 0.5




#______________PlaceHolders_________________#

ph_usuario = "Usuario"
ph_confirmar_usuario = "Confirmar Usuario"
ph_contrasena = "Contraseña"
ph_confirmar_contrasena = "Confirmar Contraseña"
ph_correo = "Correo electronico"
ph_confirmar_correo = "Confirmar Correo"
ph_nombre = "Nombres"
ph_nombre_singular = "Nombre"
ph_apellido = "Apellidos"

ph_registrar_cliente = "Registrar Cliente"

ph_confirmar = "Confirmar"
ph_guardar = "Guardar"

ph_iniciar_sesion = "Iniciar Sesión."
ph_registrarse = "Registrarse."
ph_recordar_contra = "Olvidé la contraseña."
