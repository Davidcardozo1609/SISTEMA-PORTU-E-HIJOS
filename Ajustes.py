from Constantes import *
from bd import BaseDeDatos  
from Plantilla import Clase_Plantilla
import customtkinter as ctk


class Ventana_Ajustes(Clase_Plantilla):
    def __init__(self,master,titulo="Compras",ventana_padre=None,ventana_login=None,usuario_actual=None,parent_app=None):
        
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
        
        self.Lbl_nombre_modulo.configure(text="Ajustes")
        
        
        
    