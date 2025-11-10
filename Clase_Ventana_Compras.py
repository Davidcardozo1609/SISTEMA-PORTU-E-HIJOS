#___________LIBERIAS___________________
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos  
from Plantilla import Clase_Plantilla
import customtkinter as ctk
import tkinter as tk 
from datetime import datetime
from tkinter import ttk
from Clase_Gestor_Ventanas import GestorVentanas
from Clase_Ventana_Stock import Productos

#___________CLASE COMPRAS___________________
class Compras(Clase_Plantilla):
    def __init__(self,master,titulo="Compras",ventana_padre=None,ventana_login=None,usuario_actual=None,parent_app=None):
        
        
                #En el init se definen las cosas que se van a ejecutar al instanciar la clase
                #entre parentesis ponemos lo que va a recibir,etc. algunos  estan en None para que
                #al no recibir ese valor no se rompa, por ejemplo compras no hace falta que le pasa un parent
                #pero si no le paso un master se rompe."""
                        
       
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
                #MUY IMPORTANTE: Llama al init de plantilla permitiendo tener las cosas de plantilla
                #Labels,Entrys,Frames,etc. Pero plantilla para ejecutar eso necesita que le pases
                #las cosas entre (), entonces lo que hacemos es pasarle las cosas de nuestro init a plantilla
        

        self.bd = BaseDeDatos()



    
               
        
#_______________________________FRAMES_____________________________________
        
        #Fr_Gris (ayuda a hacer el borde)
        self.Fr_help_compras = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")
        self.Fr_help_compras.place(relx=0.05, rely=0.43, relwidth=0.8, relheight=0.4)
        
        #Fr_Blanco el principal
        self.Fr_blanco_compras = ctk.CTkFrame(self.Fr_help_compras,
                                                fg_color="#ffffff" 
                                                )
        self.Fr_blanco_compras.place(relx=0.002, rely=0.002, relwidth=0.996, relheight=0.996)



        #Fr_Gris Proveedores

        self.Fr_help_proveedor = ctk.frame = ctk.CTkFrame(self.Fr_Principal,fg_color="#eaeaea")


        self.Fr_help_proveedor.place(relx=0.05, rely=0.2, relwidth=0.3,relheight=0.07)

        #Fr_Blanco de Proveedores

        self.Fr_blanco_proveedor = ctk.CTkFrame(self.Fr_help_proveedor,
                                                fg_color="#ffffff" 
                                                )
        
        self.Fr_blanco_proveedor.place(relx=0.01, rely=0.04, relwidth=0.98, relheight=0.89)


        
        self.crear_combobox()


        # Crear la tabla
        self.crear_tabla(
            self.Fr_blanco_compras,  # frame donde irá la tabla
             columnas=["Producto","Categoria","Cantidad","Precio Unitario","Subtotal"],
            con_acciones=True

        )

        
        
#__________________________BOTONES___________________________________
        
        #Boton guardar
        self.btn_guardar = ctk.CTkButton(
            self.Fr_Principal,
            text="Guardar Compra",
            fg_color="blue",
            hover_color="blue",
            font=("Arial", 20),
            command=self.guardar_compra)
        self.btn_guardar.place(relx=0.1, rely=0.85, relwidth=0.2, relheight=0.07)
        
        #Boton cancelar
        self.btn_cancelar = ctk.CTkButton(
            self.Fr_Principal,
            text="Cancelar",
            fg_color="red",
            hover_color="red",
            font=("Arial", 20),
            command=self.Cancelar
        )
        self.btn_cancelar.place(relx=0.32, rely=0.85, relwidth=0.18, relheight=0.07)
        
        self.btn_agregar = ctk.CTkButton(
            self.Fr_Principal,
            text="+ Agregar",
            fg_color="blue",
            hover_color="blue",
            font=("Arial", 24),
            command=self.abrir_menu_agregar
        )
        self.btn_agregar.place(relx=0.6, rely=0.35, relwidth=0.15, relheight=0.063)
        
    def crear_combobox(self):
        query = ("""SELECT nombre FROM proveedores""")
        self.bd.cursor.execute (query)
        self.pro = self.bd.cursor.fetchall()
        self.pro = [fila[0] for fila in self.pro]  
        print (self.pro)
        
        self.cmb_proveedor = ctk.CTkOptionMenu(self.Fr_blanco_proveedor,
                                               values=self.pro if self.pro else [""],
                                               corner_radius=6,  # bordes redondeados
                                               font=("Arial", 15, "bold"),
                                               fg_color="#fdfdfd",  # Fondo gris claro tipo placeholder
                                               button_color="#fdfdfd",# color del botón de la flecha
                                               button_hover_color="#fdfdfd",# color del botón cuando el mouse pasa encima
                                               text_color="#999999",  # Texto gris (placeholder)
                                               dropdown_fg_color="#ffffff",  # color de fondo del menú desplegable
                                               dropdown_hover_color="#e5e5e5", # color al pasar sobre una opción
                                               dropdown_text_color="black"   # color del texto en el menú desplegable
                                          )
        self.cmb_proveedor.set("Seleccionar Proveedor")
        
        self.cmb_proveedor.bind("<FocusIn>", self.on_focus)
        self.cmb_proveedor.bind("<FocusOut>", self.on_focus_out)
        
        
        
        self.cmb_proveedor.place(relx=0, rely=0, relwidth=1,relheight=1)
        
#__________________________LABELS___________________________________
        
        #Label Titulo
        self.Lbl_nombre_modulo.configure(text="Compras")
        self.Lbl_nombre_modulo.place(relx=0.05,rely=0.03,relwidth=0.18,relheight=0.1)
        #label total
        self.lbl_total = ctk.CTkLabel(self.Fr_Principal,
                                      bg_color="#ffffff",
                                      fg_color="white",
                                      font=("Arial", 25, "bold"),
                                      text="Total: $0.00")
        self.lbl_total.place(relx=0.65, rely=0.85, relwidth=0.25,relheight=0.05)
        
        #label proveedor
        self.lbl_proveedor = ctk.CTkLabel(self.Fr_Principal,
                                      text="Proveedor:",
                                      text_color="black",
                                      fg_color="white",
                                      font=("Arial", 18, "bold"))
        self.lbl_proveedor.place(relx=0.05, rely=0.15,relwidth=0.1,relheight=0.05)

        #label busqueda
        self.lbl_busqueda = ctk.CTkLabel(self.Fr_Principal,
                                      text="Busqueda de productos",
                                      text_color="black",
                                      fg_color="white",
                                      font=("Arial", 18, "bold"))
        self.lbl_busqueda.place(relx=0.05, rely=0.3,relwidth=0.22,relheight=0.05)

#__________________________STRINGVARS___________________________________
        # Variable para guardar la opción seleccionada
        self.opcion_seleccionada = ctk.StringVar(value="Seleccione proveedor")
        self.entrada_var_producto = ctk.StringVar()


#__________________________ENTRYS___________________________________     

        self.entry_busqueda = ctk.CTkEntry(self.Fr_Principal,
                                           border_color="#eaeaea",
                                           fg_color="#ffffff",
                                           placeholder_text="Ingrese el nombre del producto")

        self.entry_busqueda.place(relx=0.05,rely=0.35,relwidth=0.4,relheight=0.06)


        
#__________________________FUNCIONES___________________________________
        
    
        #________________________________PLACEHOLDER_____________________________________
    def on_focus(self,event):
        """Quita el placeholder al hacer clic."""
        if self.cmb_proveedor.get() == "Seleccionar proveedor":
            self.cmb_proveedor.set("")
            self.cmb_proveedor.configure(fg_color="white", text_color="black")

    def on_focus_out(self,event):
        """Restaura el placeholder si está vacío."""
        if self.cmb_proveedor.get() == "":
            self.cmb_proveedor.set("Seleccionar proveedor")
            self.cmb_proveedor.configure(fg_color="#f5f5f5", text_color="#999999")
            
            
            
    def abrir_menu_agregar(self):
        self.ventana_menu = ctk.CTkToplevel(self.ventana)
        self.ventana_menu.title("Agregar Producto")
        self.ventana_menu.geometry("350x300")
         # Evitar que se pueda redimensionar
        self.ventana_menu.resizable(False, False)
        self.ventana_menu.grab_set()

        # --- Labels y Entries ---
        #label producto
        self.label_producto=ctk.CTkLabel(self.ventana_menu, text="Producto:")
        self.label_producto.place(x=20, y=20)
        
        #entry producto
        self.entry_producto = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_letras_espacios,width=200 )
        self.entry_producto.place(x=140, y=20)
        
        
        #label categorias
        self.label_categorias=ctk.CTkLabel(self.ventana_menu, text="Categoría:")
        self.label_categorias.place(x=20, y=60)
        
        #entry categorias
        self.entry_categoria = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_letras_espacios,width=200 )
        self.entry_categoria.place(x=140, y=60)
        
        
        #label cantidad
        self.label_cantidad=ctk.CTkLabel(self.ventana_menu, text="Cantidad:")
        self.label_cantidad.place(x=20, y=100)
        
        #entry cantidad
        self.entry_cantidad = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.limitar_numeros,width=200 )
        self.entry_cantidad.place(x=140, y=100)
        
        #label precio unitario
        self.label_precio_unitario=ctk.CTkLabel(self.ventana_menu, text="Precio Unitario:")
        self.label_precio_unitario.place(x=20, y=140)
        
        #label precio unitario
        self.entry_precio_unitario = ctk.CTkEntry(self.ventana_menu,validate="key",validatecommand=self.validar_decimal2 ,width=200)
        self.entry_precio_unitario.place(x=140, y=140)


        # --- Botón Guardar ---
        self.guardar_menu=ctk.CTkButton(self.ventana_menu, text="Guardar", command=self.guardar_datos)
        self.guardar_menu.place(x=30, y=230)
        
        self.cancelar=ctk.CTkButton(self.ventana_menu, text="Cancelar", command=lambda:self.ventana_menu.destroy())
        self.cancelar.place(x=180, y=230)

    def guardar_datos(self):
        
        Producto = self.entry_producto.get()
        
        if Producto != "" and Producto is not None:
            pass
        else:
            ms.showwarning("Atención", "Por favor, complete el campo Producto", parent=self.ventana_menu)
            return
        
        
        
        
        cantidad = self.entry_cantidad.get()
        
        if cantidad != "" and cantidad is not None:
            cantidad = int(cantidad)
        else:
            ms.showwarning("Atención", "Por favor completa el campo Cantidad", parent=self.ventana_menu)
            return
        
        
        
        
        precio = self.entry_precio_unitario.get()
        
        if precio != "" and precio is not None:
            precio = float(precio)
        else:
            ms.showwarning("Atención", "Por favor completa el campo Precio", parent=self.ventana_menu)
            return
        
        
        
        
        
        datos = {
            "Producto": self.entry_producto.get(),
            "Categoria": self.entry_categoria.get(),
            "Cantidad": self.entry_cantidad.get(),
            "Precio Unitario": self.entry_precio_unitario.get(),
            "Subtotal": cantidad*precio
        }
        if not all(datos.values()):
            # . values() te devuelve todos los valores y all devuelve True si ninguno de los valores está vacío
            ms.showwarning("Atención", "Por favor completa todos los campos.", parent=self.ventana_menu)
            return

        
        

            
        
        if datos["Producto"] == "" or datos["Producto"].isspace():
            ms.showerror("Error", "El nombre no puede estar vacío ni contener solo espacios.", parent=self.ventana_menu)
            return
            
            
        elif not datos["Categoria"]:
            ms.showwarning("Atención", "Por favor, complete el campo Categoria", parent=self.ventana_menu)
            return
        
        elif not datos["Cantidad"]:
            ms.showwarning("Atención", "Por favor, complete el campo Cantidad", parent=self.ventana_menu)
            return
        elif not datos["Precio Unitario"]:
            ms.showwarning("Atención", "Por favor, complete el campo Precio", parent=self.ventana_menu)
            return
        else:
            self.agregar_fila(datos)


            self.actualizar_total()
            
            ms.showinfo("Exito","Datos ingresados correctamente",parent=self.ventana)
            self.ventana_menu.destroy()
            
            
            
    def guardar_compra(self):
        filas = self.tree.get_children()
        if not filas:
            ms.showwarning("Atención", "No hay productos cargados para guardar.", parent=self.ventana)
            return

        proveedor = self.cmb_proveedor.get().strip()
        if proveedor in ("", "Seleccionar proveedor"):
            ms.showwarning("Atención", "Debe seleccionar un proveedor válido.", parent=self.ventana)
            return

        # Obtener el id del proveedor
        self.bd.cursor.execute("SELECT id FROM proveedores WHERE nombre = ?", (proveedor,))
        resultado = self.bd.cursor.fetchone()
        if not resultado:
            ms.showwarning("Atención", f"No se encontró el proveedor '{proveedor}'.", parent=self.ventana)
            return
        id_proveedor = resultado[0]

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_compras = 0
        
        
        self.bd.cursor.execute("""
            INSERT INTO registro_compras(proveedor_id, proveedor, fecha, total)
            VALUES (?, ?, ?, ?)
        """, (id_proveedor, proveedor, fecha_actual, total_compras))

        # 2️⃣ Obtener el ID de esa compra
        compra_id = self.bd.cursor.lastrowid

        try:
            # 1️⃣ Insertar cada producto en compras_proveedor
            for fila_id in filas:
                valores = self.tree.item(fila_id, "values")
                fila_dict = {
                    "Producto": valores[0],
                    "Categoria": valores[1],
                    "Cantidad": valores[2],
                    "Precio Unitario": valores[3],
                    "Subtotal": valores[4]
                }

                # Validar que no haya campos vacíos
                if any(not str(v).strip() for v in fila_dict.values()):
                    ms.showwarning("Atención", "Completá todos los campos antes de guardar.", parent=self.ventana)
                    return

                # Sumar subtotal al total general
                total_compras += float(fila_dict["Subtotal"])

                # Insertar producto
                self.bd.cursor.execute("""
                    INSERT INTO compras_proveedor(proveedor_id, producto, categoria, cantidad, precio_unitario, subtotal, fecha)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_proveedor,
                    fila_dict["Producto"],
                    fila_dict["Categoria"],
                    fila_dict["Cantidad"],
                    fila_dict["Precio Unitario"],
                    fila_dict["Subtotal"],
                    fecha_actual
                ))
                self.bd.cursor.execute("""
                    INSERT INTO productos_stock(producto, categoria,  cantidad, precio_unitario,subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    
                    fila_dict["Producto"],
                    fila_dict["Categoria"],
                    fila_dict["Cantidad"],
                    fila_dict["Precio Unitario"],
                    fila_dict["Subtotal"]
                  
                ))
                
                
                self.bd.cursor.execute("""
                    INSERT INTO detalle_compras(compra_id, producto, categoria, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    compra_id,
                    fila_dict["Producto"],
                    fila_dict["Categoria"],
                    fila_dict["Cantidad"],
                    fila_dict["Precio Unitario"],
                    fila_dict["Subtotal"]
                ))
                
                self.bd.cursor.execute("""
                    UPDATE registro_compras
                    SET total = ?
                    WHERE id = ?
                """, (total_compras, compra_id))
                            
                
                self.bd.conexion.commit()

    
            
            self.bd.conexion.commit()

            self.lbl_total.configure(text=f"Total: ${total_compras:.2f}")
            self.limpiar_tabla()
            ms.showinfo("Éxito", "Compra guardada correctamente.", parent=self.ventana)
            
            if Productos in GestorVentanas.instancias:
                GestorVentanas.instancias[Productos].actualizar_tabla()
            
            Registro_Compras = __import__("Archivo_Registro_Compras").Registro_Compras

            if Registro_Compras in GestorVentanas.instancias:
                GestorVentanas.instancias[Registro_Compras].actualizar_tabla()

    


        except Exception as e:
            ms.showerror("Error", f"Ocurrió un error al guardar la compra:\n{e}", parent=self.ventana)
                
    def limpiar_tabla(self):
        """
        Elimina todas las filas de la tabla.
        """
        filas = self.tree.get_children()  # obtiene todos los IDs de fila
        for fila_id in filas:
            self.tree.delete(fila_id)      # elimina cada fila
            self.lbl_total.configure(text="Total: $0.00")

    def Cancelar(self):
        respuesta = ms.askyesno(
        "Confirmar",
        "¿Seguro que querés borrar todos los datos de la compra?"
    )
        if respuesta:
            self.limpiar_tabla()

