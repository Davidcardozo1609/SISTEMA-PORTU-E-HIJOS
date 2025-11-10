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


        self.evento_var = StringVar()
        self.hora_var = StringVar()
        
        hoy = date.today()
        self.cal = Calendar(self.Fr_Calendario,
                            selectmode='day',
                            year=hoy.year, month=hoy.month, day=hoy.day,
                            locale='es_ES',        # intenta español
                            date_pattern='dd/mm/yyyy',
                            showweeknumbers=False, #Indica si mostrar o no la columna con los números de semana
                            mindate=hoy,
                            x=500,
                            height=200)
        # El widget Calendar es un widget tkinter normal; pack/grid funciona igual
        self.cal.pack(padx=10, pady=10)
        
        # Bind: cuando se cambie la fecha
        self.cal.bind("<<CalendarSelected>>", self._on_fecha_seleccionada)

        # Label + botón para seleccionar hora
        self.label_hora = ctk.CTkLabel(self.Fr_Calendario, 
                                text="Hora", 
                                fg_color="#ffffff",
                                bg_color="#000000",
                                font=("Arial",20))
        
        self.label_hora.pack(padx=(0,200),pady=10)

        self.Fr_btns_hora = ctk.CTkFrame(self.Fr_Calendario)

        self.Fr_btns_hora.pack(padx=100, pady=10)

        self.entry_hora = ctk.CTkEntry(self.Fr_btns_hora,
                                 textvariable=self.hora_var, 
                                 state="readonly",
                                 font=("Arial",15)
                                 )
        
        self.entry_hora.pack(side="left",padx=10, pady=10)

        self.boton_hora = ctk.CTkButton(self.Fr_btns_hora, 
                                 text="Seleccionar hora", 
                                 command=self.abrir_time_picker,
                                 font=("Arial",15), 
                                 fg_color="#000000",
                                 bg_color="#ffffff",
                                 hover_color="#000000"
                                 )
        
        self.boton_hora.pack(side="right",padx=10, pady=10)


        
        # Botones para agregar / eliminar
        self.Fr_Botones = ctk.CTkFrame(self.Fr_Calendario, fg_color="transparent")
        self.Fr_Botones.pack(side="top",padx=100, pady=(0,100))
        
        self.Btn_agregar_evento = ctk.CTkButton(self.Fr_Botones, text="Agregar evento", command=self._agregar_evento)
        self.Btn_agregar_evento.pack(side="left", padx=4)

        self.Btn_eliminar_evento = ctk.CTkButton(self.Fr_Botones, text="Eliminar eventos del día")
        self.Btn_eliminar_evento.pack(side="right", padx=4)

        
        # Right: Lista de eventos y detalles
        self.Fr_reg_events = ctk.CTkFrame(self.Fr_Container)
        self.Fr_reg_events.pack(side="left", fill="both", expand=True, padx=(8,10), pady=10)
        
        self.Lbl_cal=ctk.CTkLabel(self.Fr_reg_events, text="Eventos del día", font=("Arial", 16, "bold")).pack(pady=(6,0))
        
        self.crear_tabla(
           self.Fr_reg_events,  # frame donde irá la tabla
             columnas=["Nombre del evento","Fecha","Hora"],
            con_acciones=True
        )
        
        # Inicial: mostrar eventos de hoy (si hay)
        self.actualizar_tabla(hoy)
        
        
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
        self.actualizar_tabla(fecha)
    

            
    
    def _agregar_evento(self):
        fecha = self._fecha_seleccion_obj()
        texto = simpledialog.askstring("Nuevo evento", f"Evento para {fecha.strftime('%d/%m/%Y')}:")
        self.hora_var.get()
        if texto:
            self.bd.cursor.execute(""" INSERT INTO eventos (nombre_del_evento,hora,fecha)
                                               VALUES (?,?,?) """,
                                   (texto,fecha,self.hora_var))

            
          
            
            
            # Crear marca visual en el calendario usando calevent_create (devuelve id)
            ev_id = self.cal.calevent_create(fecha, texto, 'evento')
            # Configurar estilo para la etiqueta 'evento' una sola vez
            self.cal.tag_config('evento', background='lightblue', foreground='black')
            self.actualizar_tabla(fecha)
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



    def abrir_time_picker(self):
        ventana_hora = ctk.CTkToplevel(self.ventana)
        ventana_hora.title("Seleccionar hora")
        ventana_hora.geometry("200x150")
        ventana_hora.grab_set()  # Bloquea hasta que se cierre

        hora_var = StringVar(value="00")
        minuto_var = StringVar(value="00")

        Label(ventana_hora, text="Hora:").pack(pady=(10, 0))
        spin_hora = Spinbox(ventana_hora, from_=0, to=23, textvariable=hora_var, width=5, format="%02.0f",font=("Arial", 14),state='readonly', readonlybackground='white')
        spin_hora.pack()

        Label(ventana_hora, text="Minuto:").pack()
        spin_minuto = Spinbox(ventana_hora, from_=0, to=59, textvariable=minuto_var, width=5, format="%02.0f",font=("Arial", 14),state='readonly', readonlybackground='white')
        spin_minuto.pack()

        def guardar_y_cerrar():
            hora = f"{int(hora_var.get()):02d}:{int(minuto_var.get()):02d}"
            self.hora_var.set(hora)
            ventana_hora.destroy()

        Button(ventana_hora, text="Aceptar", command=guardar_y_cerrar,font=("Arial", 14)).pack(pady=10)


    
    def actualizar_tabla(self,fecha_seleccionada):
        # Limpiar la tabla primero
        for fila in self.tree.get_children():
            self.tree.delete(fila)
            
        self.bd.cursor.execute("SELECT nombre_del_evento, hora FROM eventos WHERE fecha = ?",
                               (fecha_seleccionada,))

        resultado = self.bd.cursor.fetchall()
        for fila in resultado:
            # Suponiendo que tus columnas en Treeview son:
            # ["Producto","Categoria","Cantidad","Precio_Unitario","Subtotal","Editar","Eliminar"]
            valores = list(fila[0:6])  # Tomamos solo producto, categoria, cantidad, precio_unitario, subtotal
            valores += ["Editar", "Eliminar"]  # Añadimos botones de acción
            self.tree.insert("", "end", values=valores)
        
        
        
        
        
        

        