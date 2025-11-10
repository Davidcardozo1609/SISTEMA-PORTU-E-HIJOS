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
        self.Fr_Calendario.configure(width=300)
        self.Fr_Calendario.pack(side="left", fill="y", expand=False, padx=(10,8), pady=10)
        self.Fr_Calendario.pack_propagate(False)



 
        
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

        self.marcar_todos_los_eventos()

        


        
        # Botones para agregar / eliminar
        self.Fr_Botones = ctk.CTkFrame(self.Fr_Calendario, fg_color="transparent")
        self.Fr_Botones.pack(side="top", pady=(0,100))
        
        self.Btn_agregar_evento = ctk.CTkButton(self.Fr_Botones, text="Agregar evento", command=self._agregar_evento)
        self.Btn_agregar_evento.pack(side="left", padx=4)

        self.Btn_eliminar_evento = ctk.CTkButton(self.Fr_Botones, text="Eliminar eventos del día", command=self._eliminar_eventos_dia)
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
        ventana_eventos = ctk.CTkToplevel(self.ventana)
        ventana_eventos.title("Agregar evento")
        ventana_eventos.geometry("300x250")
        ventana_eventos.grab_set()

        fecha = self._fecha_seleccion_obj()
        evento_var = StringVar()
        hora_var = StringVar()

        # Entry nombre
        texto = ctk.CTkEntry(ventana_eventos, placeholder_text="Nombre del evento")
        texto.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.13)

        # Entry hora
        entry_hora = ctk.CTkEntry(ventana_eventos, textvariable=hora_var, state="readonly", font=("Arial", 15))
        entry_hora.place(relx=0.65, rely=0.3, relwidth=0.25, relheight=0.13)

        # Botón seleccionar hora
        ctk.CTkButton(ventana_eventos, text="Seleccionar hora", command=lambda: self.abrir_time_picker(hora_var)).place(relx=0.1, rely=0.3, relwidth=0.5, relheight=0.13)

        def guardar_y_cerrar():
            if not texto.get().strip() or texto.get() == "Nombre Del evento":
                ms.showwarning("Error", "Por favor coloque el nombre del evento", parent=ventana_eventos)
                return
            if not hora_var.get().strip():
                ms.showwarning("Error", "Por favor coloque una hora válida", parent=ventana_eventos)
                return

            self.bd.cursor.execute("INSERT INTO eventos (nombre_del_evento,hora,fecha) VALUES (?,?,?)",
                                (texto.get(), hora_var.get(), fecha))
            self.bd.conexion.commit()

            # Crear marca visual en calendario
            self.cal.calevent_create(fecha, texto.get(), 'evento')
            self.cal.tag_config('evento', background='lightblue', foreground='black')
            self.actualizar_tabla(fecha)

            # Limpiar y destruir Entry seguro
            hora_var.set("")
            entry_hora.destroy()
            ventana_eventos.destroy()

        ctk.CTkButton(ventana_eventos, text="Aceptar", command=guardar_y_cerrar).place(relx=0.25, rely=0.52, relwidth=0.5, relheight=0.13)

        
    def _eliminar_eventos_dia(self):
        fecha = self._fecha_seleccion_obj()
        fecha_iso = fecha.strftime("%Y-%m-%d")  # Formato correcto
        self.bd.cursor.execute("SELECT COUNT(*) FROM eventos WHERE fecha = ?", (fecha_iso,))

        cantidad = self.bd.cursor.fetchone()[0]

        if cantidad > 0:
            if ms.askyesno("Confirmar", f"¿Eliminar {cantidad} evento(s) del {fecha.strftime('%d/%m/%Y')}?"):
                self.bd.cursor.execute("DELETE FROM eventos WHERE fecha = ?", (fecha_iso,))
                self.bd.conexion.commit()
                self.cal.calevent_remove('evento')
                self.actualizar_tabla(fecha)
                ms.showinfo("Listo", "Eventos eliminados.")
        else:
            ms.showinfo("Info", "No hay eventos para esa fecha.")


            
            
    def Consulta_Calendario(self):
        
        self.lista.delete(0, tk.END)
        
        query= """SELECT * FROM eventos"""
        
        self.eventos= self.bd.cursor.execute(query)
        
        self.resultado=self.bd.cursor.fetchall()
        
        for fecha, descripcion in self.resultado:
            self.lista.insert(tk.END, fecha, descripcion)



    def abrir_time_picker(self, target_var):
        ventana_hora = ctk.CTkToplevel(self.ventana)
        ventana_hora.title("Seleccionar hora")
        ventana_hora.geometry("200x150")
        ventana_hora.grab_set()

        hora_var = StringVar(value="00")
        minuto_var = StringVar(value="00")

        tk.Label(ventana_hora, text="Hora:").pack(pady=(10,0))
        spin_hora = tk.Spinbox(ventana_hora, from_=0, to=23, textvariable=hora_var, width=5, format="%02.0f", font=("Arial",14), state="readonly")
        spin_hora.pack()
        tk.Label(ventana_hora, text="Minuto:").pack()
        spin_minuto = tk.Spinbox(ventana_hora, from_=0, to=59, textvariable=minuto_var, width=5, format="%02.0f", font=("Arial",14), state="readonly")
        spin_minuto.pack()

        def guardar_y_cerrar():
            target_var.set(f"{int(hora_var.get()):02d}:{int(minuto_var.get()):02d}")
            ventana_hora.destroy()

        tk.Button(ventana_hora, text="Aceptar", command=guardar_y_cerrar, font=("Arial",14)).pack(pady=10)



    
    def actualizar_tabla(self,fecha_seleccionada):
        # Limpiar la tabla primero
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        
        fecha_iso = fecha_seleccionada.strftime("%d/%m/%Y")
        
        # Limpiar eventos visuales anteriores del calendario (opcional)
        self.cal.calevent_remove('evento')

        # Configurar color de los eventos (solo una vez)
        self.cal.tag_config("evento", background="lightblue", foreground="black")

            
        self.bd.cursor.execute("SELECT id,nombre_del_evento, hora FROM eventos WHERE fecha = ?",
                               (fecha_seleccionada,))

        resultado = self.bd.cursor.fetchall()
        for id_evento ,nombre, hora in resultado:
            self.cal.calevent_create(fecha_seleccionada, nombre, "evento")
        

            valores = [nombre, fecha_seleccionada.strftime("%d/%m/%Y"), hora, "Editar", "Eliminar"]
            self.tree.insert("", "end", iid=id_evento, values=valores)

    def marcar_todos_los_eventos(self):
        # Borra marcas anteriores
        self.cal.calevent_remove('evento')

        # Consulta TODAS las fechas que tienen eventos
        self.bd.cursor.execute("SELECT nombre_del_evento, fecha FROM eventos")
        eventos = self.bd.cursor.fetchall()

        # Recorre los resultados y crea marcas visuales
        for nombre, fecha_texto in eventos:
            # Convertir texto de la base a objeto date
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()

            # Crear evento visual en el calendario
            self.cal.calevent_create(fecha, nombre, "evento")

        # Configurar color del tag
        self.cal.tag_config("evento", background="lightblue", foreground="black")

    def editar_producto(self, valores, fila_id):
        ventana_eventos = ctk.CTkToplevel(self.ventana)
        ventana_eventos.title("Editar evento")
        ventana_eventos.geometry("300x250")
        ventana_eventos.grab_set()

        nombre_actual, fecha_str, hora_actual = valores[0], valores[1], valores[2]
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        hora_var = StringVar(value=hora_actual)

        texto = ctk.CTkEntry(ventana_eventos, placeholder_text="Nombre del evento")
        texto.insert(0, nombre_actual)
        texto.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.13)

        entry_hora = ctk.CTkEntry(ventana_eventos, textvariable=hora_var, state="readonly", font=("Arial",15))
        entry_hora.place(relx=0.65, rely=0.3, relwidth=0.25, relheight=0.13)

        ctk.CTkButton(ventana_eventos, text="Seleccionar hora", command=lambda: self.abrir_time_picker(hora_var)).place(relx=0.1, rely=0.3, relwidth=0.5, relheight=0.13)

        def guardar_y_cerrar():
            nuevo_nombre = texto.get()
            nueva_hora = hora_var.get()

            if not nuevo_nombre.strip():
                ms.showwarning("Error", "Ingrese nombre del evento", parent=ventana_eventos)
                return
            if not nueva_hora.strip():
                ms.showwarning("Error", "Ingrese hora válida", parent=ventana_eventos)
                return

            self.bd.cursor.execute("UPDATE eventos SET nombre_del_evento=?, hora=? WHERE id=? AND fecha=?",
                                (nuevo_nombre, nueva_hora, fila_id, fecha.strftime("%Y-%m-%d")))
            self.bd.conexion.commit()

            self.actualizar_tabla(fecha)
            self.marcar_todos_los_eventos()
            ms.showinfo("Éxito", "Evento actualizado correctamente.")

            hora_var.set("")
            entry_hora.destroy()
            ventana_eventos.destroy()

        ctk.CTkButton(ventana_eventos, text="Aceptar", command=guardar_y_cerrar).place(relx=0.25, rely=0.52, relwidth=0.5, relheight=0.13)

            
        
    def eliminar_producto(self, row_id, valores):
        respuesta = ms.askyesno("Eliminar", f"¿Seguro que querés eliminar {valores[0]}?", parent=self.ventana)
        if respuesta:
            # Borrar de la base de datos
            self.bd.cursor.execute("DELETE FROM eventos WHERE id = ?", (row_id,))
            self.bd.conexion.commit()
            
            # Borrar de la tabla visual
            self.tree.delete(row_id)
            
            # Borrar el evento visual del calendario
            self.cal.calevent_remove('evento')  # quita todos los eventos del tag 'evento'
            
            # Volver a marcar los eventos restantes
            self.marcar_todos_los_eventos()
            
            ms.showinfo("Eliminado", f"{valores[0]} fue eliminado.", parent=self.ventana)




            
            
            
            
            
            

            