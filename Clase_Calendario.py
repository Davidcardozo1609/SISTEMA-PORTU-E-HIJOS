from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos
from tkcalendar import Calendar
from datetime import datetime, date
from Plantilla import Clase_Plantilla
import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog




class Calendario(Clase_Plantilla):
    def __init__(self,master,titulo,ventana_padre, ventana_login, usuario_actual=None, parent_app=None):
        # Llamamos al constructor de Stock con sus parámetros
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
        
        self.Lbl_nombre_modulo.destroy()
        
        self.bd = BaseDeDatos()
        
        
        
        
        # Frame principal
        self.Fr_Container = ctk.CTkFrame(self.Fr_Principal, corner_radius=12)
        self.Fr_Container.pack(fill="both", expand=True)
        
        # Left: Calendar
        self.Fr_Calendario = ctk.CTkFrame(self.Fr_Container)
        self.Fr_Calendario.pack(side="left", fill="both", expand=False, padx=(10,8), pady=10)
        
        hoy = date.today()
        self.cal = Calendar(self.Fr_Calendario,
                            selectmode='day',
                            year=hoy.year, month=hoy.month, day=hoy.day,
                            locale='es_ES',        # intenta español
                            date_pattern='dd/mm/yyyy',
                            showweeknumbers=False)
        # El widget Calendar es un widget tkinter normal; pack/grid funciona igual
        self.cal.pack(padx=10, pady=10)
        
        # Bind: cuando se cambie la fecha
        self.cal.bind("<<CalendarSelected>>", self._on_fecha_seleccionada)
        
        # Botones para agregar / eliminar
        self.Fr_Botones = ctk.CTkFrame(self.Fr_Calendario, fg_color="transparent")
        self.Fr_Botones.pack(fill="x", padx=10, pady=(0,100))
        
        self.Btn_agregar_evento=ctk.CTkButton(self.Fr_Botones, text="Agregar evento", command=self._agregar_evento).pack(side="left", padx=4)
        
        self.Btn_agregar_evento=ctk.CTkButton(self.Fr_Botones, text="Eliminar eventos del día").pack(side="left", padx=4)
        
        # Right: Lista de eventos y detalles
        self.Fr_reg_events = ctk.CTkFrame(self.Fr_Container)
        self.Fr_reg_events.pack(side="left", fill="both", expand=True, padx=(8,10), pady=10)
        
        self.Lbl_cal=ctk.CTkLabel(self.Fr_reg_events, text="Eventos del día", font=("Arial", 16, "bold")).pack(pady=(6,0))
        
        self.lista = tk.Listbox(self.Fr_reg_events, height=15)  # uso Listbox tkinter para más control
        self.lista.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Inicial: mostrar eventos de hoy (si hay)
        self._refrescar_lista_para_fecha(hoy)
        
        
    def _fecha_seleccion_obj(self):
        """Devuelve datetime.date de la fecha seleccionada."""
        try:
            return self.cal.selection_get()
        except Exception:
            # fallback: parsear get_date()
            s = self.cal.get_date()  # string dd/mm/yyyy si date_pattern lo puso así
            return datetime.strptime(s, "%d/%m/%Y").date()
    
    def _on_fecha_seleccionada(self, event=None):
        fecha = self._fecha_seleccion_obj()
        self._refrescar_lista_para_fecha(fecha)
    
    def _refrescar_lista_para_fecha(self, fecha: date):
        self.lista.delete(0, tk.END)
        eventos = self.bd.cursor.execute("""SELECT descripcion FROM eventos WHERE fecha = ?""", (fecha,))
        if not eventos:
            self.lista.insert(tk.END, "(sin eventos)")
        else:
            for descripcion in eventos:
                self.lista.insert(tk.END, descripcion)
    
    def _agregar_evento(self):
        fecha = self._fecha_seleccion_obj()
        texto = simpledialog.askstring("Nuevo evento", f"Evento para {fecha.strftime('%d/%m/%Y')}:")
        if texto:
            self.bd.cursor.execute(""" INSERT INTO eventos (fecha,descripcion)
                                               VALUES (?,?) """,
                                   (fecha,texto))

            
          
            
            
            # Crear marca visual en el calendario usando calevent_create (devuelve id)
            ev_id = self.cal.calevent_create(fecha, texto, 'evento')
            # Configurar estilo para la etiqueta 'evento' una sola vez
            self.cal.tag_config('evento', background='lightblue', foreground='black')
            self._refrescar_lista_para_fecha(fecha)
        else:
            ms.showinfo("Info", "Evento vacío, no se guardó.")
    
    def _eliminar_eventos_dia(self):
        fecha = self._fecha_seleccion_obj()
        if fecha in self.eventos:
            if ms.askyesno("Confirmar", f"Eliminar {len(self.eventos[fecha])} evento(s) para {fecha.strftime('%d/%m/%Y')}?"):
                # borrar eventos del almacenamiento
                del self.eventos[fecha]
                # borrar eventos del calendario (por tag o por fecha)
                # calevent_remove puede recibir un tag:
                self.cal.calevent_remove('evento')  # Ojo: esto quita todos los eventos con tag 'evento'
                # mejor: podrías iterar los eventos y borrar por id si los guardás
                self._refrescar_lista_para_fecha(fecha)
        else:
            ms.showinfo("Info", "No hay eventos para esa fecha.")
            
            
    def Consulta_Calendario(self):
        
        self.lista.delete(0, tk.END)
        
        query= """SELECT * FROM eventos"""
        
        self.eventos= self.bd.cursor.execute(query)
        
        self.resultado=self.bd.cursor.fetchall()
        
        for fecha, descripcion in self.resultado:
            self.lista.insert(tk.END, fecha, descripcion)
        
        
        
        
        
        

        