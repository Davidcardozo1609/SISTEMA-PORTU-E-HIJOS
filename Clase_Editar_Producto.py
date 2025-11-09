import sqlite3 as sqlcon
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos



class EditarProducto(Toplevel):
    def __init__(self, parent_app, datos_producto):
        super().__init__(parent_app.Stock)
        self.title("Editar Producto")
        self.geometry("300x250")
        self.resizable(False, False)
        
        self.bd = BaseDeDatos()
        
        self.transient(parent_app.Stock)
        self.grab_set()
        self.focus()

        self.parent_app = parent_app
        self.datos_producto = datos_producto
        
        
        self.numeros = self.register(self.validar_numero_y_longitud)
        self.vcmd = self.register(self.validar_letras_espacios_y_longitud)
        self.validar_decimal = self.register(self.validar_decimal_y_longitud)

        # Label y Entry para Nombre
        self.label_nombre = Label(self, text="PRODUCTO:")
        self.label_nombre.pack(pady=(10, 0))
        self.entry_nombre = Entry(self, bg="white", bd=0, relief="solid", font=("Arial", 15),
                                  validate="key", validatecommand=(self.vcmd, '%P'))
        self.entry_nombre.bind("<KeyRelease>", self.formatear_entry_nombre)
        self.entry_nombre.pack()
        self.entry_nombre.insert(0, datos_producto[1])

        # PRECIO
        self.label_precio = Label(self, text="PRECIO:")
        self.label_precio.pack(pady=(10, 0))
        self.entry_precio = Entry(self, bg="white", bd=0, relief="solid", font=("Arial", 15),
                                  validate="key", validatecommand=(self.validar_decimal, '%P'))
        self.entry_precio.pack()
        self.entry_precio.configure(validate="none")
        self.entry_precio.insert(0, str(datos_producto[2]))  # Asumiendo que [2] es el precio
        self.entry_precio.configure(validate="key")

        # STOCK
        self.label_stock = Label(self, text="STOCK:")
        self.label_stock.pack(pady=(10, 0))
        self.entry_stock = Entry(self, bg="white", bd=0, relief="solid", font=("Arial", 15),
                                 validate="key", validatecommand=(self.numeros, '%P'))
        self.entry_stock.pack()
        self.entry_stock.configure(validate="none")
        self.entry_stock.insert(0, str(datos_producto[3]))  # Asumiendo que [3] es el stock
        self.entry_stock.configure(validate="key")


        # Botón Guardar
        self.boton_guardar = Button(self, text="Guardar Cambios", command=self.guardar_cambios)
        self.boton_guardar.pack(pady=(15, 5))

        # Botón Cancelar
        self.boton_cancelar = Button(self, text="Cancelar", command=self.cancelar)
        self.boton_cancelar.pack()
        
    def cancelar(self):
        self.destroy()

        
        
    def formatear_texto(self, texto):
        # No usamos split() porque borra espacios consecutivos
        resultado = []
        mayus = True
        for c in texto:
            if mayus and c.isalpha():
                resultado.append(c.upper())
                mayus = False
            else:
                resultado.append(c.lower())
                if c == " ":
                    mayus = True
        return "".join(resultado)

    def formatear_entry_nombre(self, event=None):
        texto = self.entry_nombre.get()
        texto_formateado = self.formatear_texto(texto)
        if texto != texto_formateado:
            pos = self.entry_nombre.index(INSERT)
            self.entry_nombre.delete(0, END)
            self.entry_nombre.insert(0, texto_formateado)
            self.entry_nombre.icursor(pos)
        
    def validar_letras_espacios_y_longitud(self, texto):
        return all(c.isalpha() or c.isspace() for c in texto) and len(texto) <= 40
    
    def validar_numero_y_longitud(self, texto):
        return (texto.isdigit() or texto == "") and len(texto) <= 15
        
    def validar_decimal_y_longitud(self, texto):
        if texto == "":
            return True
        try:
            float(texto)
            if texto.count('.') > 1:
                return False
            if '.' in texto:
                parte_decimal = texto.split('.')[1]
                if len(parte_decimal) > 2:
                    return False
            return len(texto) <= 8
        except ValueError:
            return False


    def guardar_cambios(self):
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_stock.get().strip()
        precio = self.entry_precio.get().strip()


        if not nombre or not cantidad or not precio:
            ms.showwarning("Error", "Todos los campos deben estar completos.",parent=self)
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            ms.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal.", parent=self)
            return

        # Verificar si el nombre nuevo ya existe en otro producto
        self.bd.cursor.execute("SELECT id, cantidad, precio FROM productos_stock WHERE LOWER(producto) = LOWER(?) AND id != ?", (nombre.lower(), self.datos_producto[0]))
        resultado = self.bd.cursor.fetchone()

        if resultado:
            id_existente, cantidad_existente, precio_existente = resultado
            nueva_cantidad = cantidad_existente + cantidad

            ms.showinfo("Producto ya existente", f"'{nombre}' ya tiene {cantidad_existente} unidades a ${precio_existente}.",parent=self)
            respuesta = ms.askquestion("Actualizar precio", f"¿Querés cambiar el precio a ${precio}?",parent=self)

            if respuesta == "yes":
                self.bd.cursor.execute("UPDATE productos_stock SET cantidad = ?, precio = ? WHERE id = ?",
                               (nueva_cantidad, precio, id_existente))
                self.bd.conexion.commit()
                ms.showinfo("Actualizado", f"Se sumaron {cantidad} unidades y se actualizó el precio a ${precio}.",parent=self)
            else:
                self.bd.cursor.execute("UPDATE productos_stock SET cantidad = ? WHERE id = ?",
                               (nueva_cantidad, id_existente))
                self.bd.conexion.commit()
                ms.showinfo("Actualizado", f"Se sumaron {cantidad} unidades y se mantuvo el precio anterior (${precio_existente}).",parent=self)

            # Eliminar el producto original si es diferente al actualizado
            self.bd.cursor.execute("DELETE FROM productos_stock WHERE id = ?", (self.datos_producto[0],))
            self.bd.conexion.commit()

        else:
            # Nombre no duplicado: actualizar normalmente el producto original
            self.bd.cursor.execute("UPDATE productos_stock SET producto = ?, cantidad = ?, precio = ? WHERE id = ?",
                           (nombre, cantidad, precio, self.datos_producto[0]))
            self.bd.conexion.commit()
            
        ms.showinfo("Actualizado", "Producto actualizado correctamente.", parent=self)
        
        self.destroy()
        
        self.parent_app.mostrar_datos_guardados()
   

