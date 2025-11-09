import sqlite3 as sqlcon
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos


class EditarCliente(Toplevel):
    def __init__(self, datos, parent_app):
        super().__init__(parent_app.Stock)
        self.datos = datos
        self.app = parent_app  # referencia a self en Clientes (para acceder a vcmd y métodos)
        self.title("Modificar Cliente")
        self.geometry("400x400")
        self.resizable(False, False)
        
        self.bd = parent_app.bd

    
        
        
        self.transient(parent_app.Stock)
        self.grab_set()
        self.focus()

        self.crear_widgets()

    def crear_widgets(self):
        # Nombre
        Label(self, text="Nombre:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_nombre = Entry(self, font=("Arial", 15), validate="key",
                                  validatecommand=(self.app.vcmd_letras, '%P'))
        self.entry_nombre.bind("<FocusOut>", lambda e: self.app.capitalizar_entrada(self.entry_nombre))
        self.entry_nombre.pack(fill="x", padx=10)
        self.entry_nombre.insert(0, self.datos[0])

        # Apellido
        Label(self, text="Apellido:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_apellido = Entry(self, font=("Arial", 15), validate="key",
                                    validatecommand=(self.app.vcmd_letras, '%P'))
        self.entry_apellido.bind("<FocusOut>", lambda e: self.app.capitalizar_entrada(self.entry_apellido))
        self.entry_apellido.pack(fill="x", padx=10)
        self.entry_apellido.insert(0, self.datos[1])

        # DNI
        Label(self, text="DNI:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_dni = Entry(self, font=("Arial", 15), validate="key",
                               validatecommand=(self.app.vcmd_dni, '%P'))
        self.entry_dni.pack(fill="x", padx=10)
        self.entry_dni.insert(0, self.datos[2])

        # Email
        Label(self, text="Email:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_email = Entry(self, font=("Arial", 15), validate="key",
                                 validatecommand=(self.app.vcmd_email, '%P'))
        self.entry_email.pack(fill="x", padx=10)
        self.entry_email.insert(0, self.datos[3])

        # Teléfono
        Label(self, text="Teléfono:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_telefono = Entry(self, font=("Arial", 15), validate="key",
                                    validatecommand=(self.app.vcmd_telefono, '%P'))
        self.entry_telefono.pack(fill="x", padx=10)
        self.entry_telefono.insert(0, self.datos[4])

        Button(self, text="Guardar cambios", command=self.guardar_cambios,
               bg="green", fg="white").pack(pady=15)
        
                # Botón Cancelar
        Button(self, text="Cancelar", command=self.cancelar, bg="gray", fg="white").pack(pady=(0, 10))
        
    def cancelar(self):
        self.destroy()




    def guardar_cambios(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        nuevo_dni = self.entry_dni.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        dni_original = self.datos[2]
        
        

        if not all([nombre, apellido, nuevo_dni, email, telefono]):
            ms.showwarning("Atención", "Todos los campos son obligatorios.",parent=self)
            return

        if not nuevo_dni.isdigit() or not (9 <= len(nuevo_dni) <= 10):
            ms.showerror("DNI inválido", "El DNI debe contener solo números y tener entre 9 y 10 dígitos.",parent=self)
            return

        if email.count("@") != 1:
            ms.showerror("Correo inválido", "El correo debe contener un único '@'.",parent=self)
            return

        parte_local, dominio = email.split("@")
        if len([c for c in parte_local if c.isalpha()]) < 1:
            ms.showerror("Correo inválido", "Debe haber al menos 1 letra antes del '@'.",parent=self)
            return

        # Verificar duplicado si DNI cambió
        if nuevo_dni != dni_original:
            self.bd.cursor.execute("SELECT dni FROM clientes WHERE dni = ?", (nuevo_dni,))
            if self.bd.cursor.fetchone():
                ms.showerror("DNI duplicado", f"Ya existe un cliente con el DNI {nuevo_dni}.",parent=self)
                return

        try:
            self.bd.cursor.execute("""
                UPDATE clientes
                SET nombre = ?, apellido = ?, dni = ?, email = ?, telefono = ?
                WHERE dni = ?
            """, (nombre, apellido, nuevo_dni, email, telefono, dni_original))
            self.bd.conexion.commit()
            self.destroy()
            ms.showinfo("Éxito", "Cliente actualizado correctamente.",parent=self.app.Stock)
            self.app.limpiar_resultados()
            self.app.cargar_clientes_guardados()
        except Exception as e:
            ms.showerror("Error", f"No se pudo actualizar: {e}",parent=self)
            


