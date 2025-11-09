from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import re
from tkcalendar import Calendar
from datetime import datetime, date
import sys, os
from tkinter import simpledialog
import shutil
from Clase_Ventana_Stock import Stock
from bd import BaseDeDatos
from Clase_Calendario import Calendario

class RegistroCalendario(Stock):
    def __init__(self, ventana_padre, ventana_login, usuario_actual, parent_app=None):
        # Llamamos al constructor de Stock con sus parámetros
        super().__init__(ventana_padre, ventana_login, usuario_actual)

        # Guardamos la referencia al menú principal (opcional)
        self.parent_app = parent_app   

        try:
            self.entry_busqueda.destroy()
            self.boton_buscar.destroy()
            self.boton_mostrar_todo.destroy()
            self.boton_eliminar.destroy()
        except:
            pass

        self.Stock.title("Registro de eventos")
        self.stock_label.config(text="Registro De Eventos")
        
        self.Frame_del_canva.place(relx=0.05,rely=0.2,relwidth=0.85,relheight=0.6)

        
      
        

            # Botón de volver al calendario
        self.flecha_stock = Button(
            self.Stock,
            image=self.flecha_tk,
            bg="white",
            activebackground="lightgray",
            relief="flat",
            bd=0,
            command=self.volver_a_calendario   # ✅ en vez de ir_a_pantalla_x(...)

        )
        self.flecha_stock.place(relx=0.02, rely=0.01, relwidth=0.047, relheight=0.085)
        
        self.cargar_eventos()

    def cargar_eventos(self):
        try:
            self.bd.cursor.execute("SELECT rowid, fecha, hora, descripcion FROM eventos ORDER BY fecha, hora")
            eventos = self.bd.cursor.fetchall()

            for widget in self.frame_datos.winfo_children():
                widget.destroy()
                
                
            columnas = ["FECHA", "HORA", "NOMBRE DE EVENTOS"]
            for col, nombre in enumerate(columnas):
                Label(self.frame_datos, text=nombre, bg="deeppink", fg="white", width=20).grid(row=0, column=col, sticky="ew")
                self.frame_datos.grid_columnconfigure(col, weight=1)

            if eventos:
                for x, fila in enumerate(eventos):
                    (rowid, fecha, hora, descripcion) = fila
                    

                    # Mostrar fecha, hora y descripción
                    Label(self.frame_datos, text=fecha, font=("Arial", 12)).grid(row=x+1, column=0, padx=5, pady=3,sticky="nsew")
                    Label(self.frame_datos, text=hora, font=("Arial", 12)).grid(row=x+1, column=1, padx=5, pady=3, sticky="nsew")
                    Label(self.frame_datos, text=descripcion, font=("Arial", 12), wraplength=280).grid(row=x+1, column=2, padx=5, pady=3, sticky="nsew")

                    # Botones dentro de un mismo frame en la columna 3
                    frame_botones = Frame(self.frame_datos)
                    frame_botones.grid(row=x+1, column=3, padx=5, pady=3, sticky="e")

                    Button(frame_botones, text="Eliminar", bg="red", fg="white", command=lambda id=rowid: self.eliminar_evento(id)).pack(side="left", padx=2)
                    Button(frame_botones, text="Modificar", bg="orange", fg="black",
                           command=lambda id=rowid, f=fecha, d=descripcion: self.modificar_evento(id, f, d)).pack(side="left", padx=2)


            else:
                Label(self.frame_datos, text="No hay eventos guardados.", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        except Exception as e:
            ms.showerror("Error", f"No se pudo cargar el registro:\n{e}",parent=self.Stock)

    def eliminar_evento(self, rowid):
        confirmar = ms.askyesno("Confirmar eliminación", "¿Querés eliminar este evento?",parent=self.Stock)
        if confirmar:
            try:
                self.bd.cursor.execute("DELETE FROM eventos WHERE rowid = ?", (rowid,))
                self.bd.conexion.commit()
                self.cargar_eventos()
                ms.showinfo("Evento eliminado", "Evento eliminado correctamente.",parent=self.Stock)
            except Exception as e:
                ms.showerror("Error", f"No se pudo eliminar el evento:\n{e}",parent=self.Stock)

    def modificar_evento(self, rowid, fecha, descripcion_anterior):
        ventana_mod = Toplevel(self.Stock)
        ventana_mod.title(f"Modificar evento del {fecha}")
        ventana_mod.geometry("550x200")
        ventana_mod.minsize(width=550, height=200)
        ventana_mod.grab_set()

        # Entry en vez de Text
        self.txt_mod = Entry(ventana_mod, font=("Arial", 19), width=50,validate="key", validatecommand=(self.vcmd_let_long, '%P'))
        self.txt_mod.pack(padx=10, pady=20,ipady=35,)
        self.txt_mod.insert(0, descripcion_anterior)
        self.txt_mod.focus_set()
        self.txt_mod.bind("<KeyRelease>", self.formatear_entry_nombre)

        # --- Guardar modificación ---
        def guardar_modificacion():
            nuevo = self.txt_mod.get().strip()
            if len(nuevo) == 0:
                ms.showwarning("Límite", "El evento no puede estar vacío.")
                return
            if len(nuevo) > 150:
                ms.showwarning("Límite", "El evento no puede tener más de 150 caracteres.")
                return
            self.bd.cursor.execute("UPDATE eventos SET descripcion = ? WHERE rowid = ?", (nuevo, rowid))
            self.bd.conexion.commit()
            self.cargar_eventos()
            ventana_mod.destroy()
            ms.showinfo("Evento modificado", f"Evento del {fecha} modificado correctamente.", parent=self.Stock)

        Button(ventana_mod, text="Guardar", font=("Arial", 16), command=guardar_modificacion).pack(pady=10)
        
    def formatear_entry_nombre(self, event=None):
        texto = self.txt_mod.get()
        texto_formateado = self.formatear_texto(texto)
        if texto != texto_formateado:
            pos = self.txt_mod.index(INSERT)
            self.txt_mod.delete(0, END)
            self.txt_mod.insert(0, texto_formateado)
            self.txt_mod.icursor(pos)





    def volver_a_calendario(self):
        # Cerramos Registro y abrimos un Calendario "limpio"
        self.Stock.destroy()
        Calendario(
            ventana_padre=self.menu_principal,   # ✅ el MENÚ PRINCIPAL real
            ventana_login=self.ventana_login,
            usuario_actual=self.usuario_actual,
            parent_app=self.menu_principal
        )


    # Botón Guardar
        

        
