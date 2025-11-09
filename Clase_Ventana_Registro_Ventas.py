
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos  
from Clase_Ventana_Stock import Stock


class RegistroVentas(Stock):
    def __init__(self, ventana_padre, ventana_login, usuario_actual, parent_app=None):
        # Llamamos al constructor de Stock con sus parámetros
        super().__init__(ventana_padre, ventana_login, usuario_actual)

        # Guardamos la referencia al menú principal (opcional)
        self.parent_app = parent_app        
        
        

        
        self.Stock.title("Registro de Ventas")
        self.stock_label.config(text="Registro De Ventas")
        
        self.Frame_del_canva.place_forget()
        self.entry_busqueda.destroy()
        self.boton_buscar.destroy()

               
        
        self.flecha_stock.config(command=self.volver_a_ventas)
        
        Label(self.pag_stock, text="REGISTRO DE VENTAS", bg="#ac196f", fg="white", font=("Arial", 20)).pack(fill="x")
        
        self.frame_para_registro= Frame(self.Stock,bg="#e51e92") # Color de fondo para ver si algo falla
        self.frame_para_registro.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        self.frame_tabla = Frame(self.frame_para_registro, bg="#e51e92")
        self.frame_tabla.pack(fill="both", expand=True)

        self.canvas = Canvas(self.frame_tabla, bg="#e51e92", highlightthickness=0)
        self.scrollbar = Scrollbar(self.frame_tabla, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # 🔧 Frame dentro del canvas (contenido)
        self.frame_datos2 = Frame(self.canvas, bg="#e51e92")
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.frame_datos2, anchor="nw")

        # 🔁 Ajuste automático
        self.frame_datos2.bind("<Configure>", self.actualizar_scrollregion)
        self.canvas.bind("<Configure>", self.ajustar_ancho_frame)
        
                # Entry para ID de registro a eliminar
        # Entry para nombre del producto a eliminar
        self.vcmd_busqueda = self.Stock.register(self.validar_letras_espacios_y_longitud)

        # Entry de búsqueda con validación
        self.entry_busqueda = Entry(self.Stock, 
                                    font=("Arial", 12),
                                    validate="key", 
                                    validatecommand=(self.vcmd_busqueda, '%P'))
        self.entry_busqueda.place(relx=0.25, rely=0.13, relwidth=0.4,relheight=0.06)
        
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_registros)

        self.buscar_label = Label(self.Stock, text="Buscar", font=("Arial", 12))
        self.buscar_label.place(relx=0.13, rely=0.13, relwidth=0.1, relheight=0.06)
        

        self.ultimo_registro_eliminado = None  # para guardar el último registro eliminado

        self.cargar_registros()
        
                # Primero eliminamos el tooltip actual si existe
        if self.flecha_stock in self.tooltips:
            self.hide_tooltip(self.flecha_stock)

        # Luego agregamos uno nuevo con el texto actualizado
        self.add_tooltip(self.flecha_stock, "Volver a Ventas")


    def actualizar_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def ajustar_ancho_frame(self, event):
        self.canvas.itemconfig(self.canvas_window_id, width=event.width)

    def cargar_registros(self, filtro=""):
        for widget in self.frame_datos2.winfo_children():
            widget.destroy()

        columnas = ["FECHA", "PRODUCTO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "GANANCIA", "ELIMINAR"]
        
        for col, nombre in enumerate(columnas):
            label = Label(self.frame_datos2, text=nombre, bg="deeppink", fg="white", font=("Arial", 12))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            self.frame_datos2.grid_columnconfigure(col, weight=1)

        if filtro:
            self.bd.cursor.execute("""
                SELECT id, fecha, producto, cantidad, precio_compra, precio, total 
                FROM ventas 
                WHERE producto LIKE ? 
                ORDER BY fecha DESC
            """, (f"%{filtro}%",))
        else:
            self.bd.cursor.execute("SELECT id, fecha, producto, cantidad, precio_compra, precio, total FROM ventas ORDER BY fecha DESC")

        filas = self.bd.cursor.fetchall()


        # ✅ Mostrar mensaje si no hay resultados
        if not filas:
            Label(self.frame_datos2, text="No se encontraron ventas.", bg="#e51e92", fg="white",
                  font=("Arial", 14, "bold")).grid(row=1, column=0, columnspan=len(columnas), pady=20)
            return

        # Mostrar cada fila
        for i, fila in enumerate(filas):
            id_registro, fecha, producto, cantidad, precio_compra, precio_venta, total_guardado = fila
            
            try:
                cantidad_num = int(cantidad)
                precio_compra_num = float(precio_compra)
                precio_venta_num = float(precio_venta)
                total_calculado = round((precio_venta_num - precio_compra_num) * cantidad_num, 2)
            except (ValueError, TypeError):
                total_calculado = 0.0

            datos = [fecha, producto, cantidad, precio_compra, precio_venta, total_calculado]

            for j, valor in enumerate(datos):
                Label(self.frame_datos2, text=valor, bg="#f0f0f0", fg="black", font=("Arial", 12)).grid(
                    row=i + 1, column=j, padx=5, pady=2, sticky="nsew")

            btn_eliminar = Button(self.frame_datos2, text="X", fg="white", bg="red", font=("Arial", 10),
                                  command=lambda id_reg=id_registro: self.eliminar_registro_por_id(id_reg))
            btn_eliminar.grid(row=i + 1, column=len(datos), padx=5, pady=2, sticky="nsew")
            self.add_tooltip(btn_eliminar, "Eliminar Venta")

            
            
    def filtrar_registros(self, event):
        texto = self.entry_busqueda.get().strip()
        self.cargar_registros(filtro=texto)




    def eliminar_registro_por_id(self, id_registro):
        respuesta = ms.askyesno("Confirmar", "¿Querés eliminar este registro?",parent=self.Stock)
        if respuesta:
            self.bd.cursor.execute("DELETE FROM ventas WHERE id = ?", (id_registro,))
            self.bd.conexion.commit()
            self.cargar_registros()
            ms.showinfo("Éxito", "Registro eliminado correctamente.",parent=self.Stock)


    def volver_a_ventas(self):
        self.Stock.destroy()         # cerramos RegistroVentas
        self.ventana_padre.deiconify()# volvemos a mostrar la ventana Ventas
        self.ventana_padre.state('zoomed')

           
    def eliminar_registro(self):
        nombre_producto = self.entry_nombre.get().strip()
        if not nombre_producto:
            ms.showerror("Error", "Ingresá un nombre de producto.",parent=self.Stock)
            return

        self.bd.cursor.execute("""
            SELECT * FROM ventas 
            WHERE producto = ? 
            ORDER BY fecha DESC LIMIT 1
        """, (nombre_producto,))
        fila = self.bd.cursor.fetchone()

        if fila:
            self.ultimo_registro_eliminado = fila  # guardo para deshacer
            self.bd.cursor.execute("DELETE FROM ventas WHERE id = ?", (fila[0],))
            self.bd.conexion.commit()
            self.entry_nombre.delete(0, END)
            self.cargar_registros()
            ms.showinfo("Éxito", f"Se eliminó el último registro de '{nombre_producto}'.",parent=self.Stock)
        else:
            ms.showerror("Error", f"No se encontró ningún registro con el producto '{nombre_producto}'.",parent=self.Stock)
    
    def calcular_total(self, cantidad, precio_venta):
        try:
            cantidad_num = int(cantidad)
            precio_num = float(precio_venta)
            return round(cantidad_num * precio_num, 2)
        except (ValueError, TypeError):
            return 0.0



       
    def reintegrar_a_stock(self):
        nombre_producto = self.entry_nombre.get().strip()
        if not nombre_producto:
            ms.showerror("Error", "Ingresá un nombre de producto.",parent=self.Stock)
            return

        # Busco el último registro de ventas por producto
        self.bd.cursor.execute("""
            SELECT * FROM ventas 
            WHERE producto = ? 
            ORDER BY fecha DESC LIMIT 1
        """, (nombre_producto,))
        venta = self.bd.cursor.fetchone()

        if venta:
            _, _, producto, cantidad, precio, _ = venta

            # 1. Eliminar de ventas
            self.bd.cursor.execute("DELETE FROM ventas WHERE id = ?", (venta[0],))

            # 2. Devolver al stock
            # cuando leas stock
            self.bd.cursor.execute("SELECT cantidad FROM productos_stock WHERE producto = ?", (producto,))
            resultado = self.bd.cursor.fetchone()
            if resultado:
                nuevo_stock = resultado[0] + cantidad
                self.bd.cursor.execute(
                    "UPDATE productos_stock SET cantidad = ?, precio = ? WHERE producto = ?",
                    (nuevo_stock, precio, producto)
                )
            else:
                self.bd.cursor.execute(
                    "INSERT INTO productos_stock (producto, precio, cantidad) VALUES (?, ?, ?)",
                    (producto, precio, cantidad)
                )

                
    def validar_letras_espacios_y_longitud(self, texto):
        return all(c.isalpha() or c.isspace() for c in texto) and len(texto) <= 30
        