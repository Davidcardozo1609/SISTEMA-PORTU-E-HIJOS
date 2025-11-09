from Plantilla import Clase_Plantilla
from tkinter import ttk, Button, Label, Entry, Frame
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox as ms
import sys, os
from Constantes import *
from bd import BaseDeDatos  

# REFERENCIAS

# btn = boton
# reg_cli = Registrar cliente
# lbl = label
# ent = entry
# cli = cliente
# reg = registro

# --- Clientes --- #   
class Clientes(Clase_Plantilla):
    def __init__(self,master,titulo,ventana_padre,ventana_login,usuario_actual=None,parent_app=None):
        super().__init__(master=master,
                         titulo=titulo,
                         ventana_padre=ventana_padre,
                         usuario_actual=usuario_actual,
                         parent_app=parent_app)
        
        self.ventana.title("Clientes")

        self.Lbl_nombre_modulo.configure(text="Clientes", anchor="w", fg_color="#fdfdfd")

        self.bd = BaseDeDatos()
    
        style = ttk.Style()

        # LISTA DE CLIENTES

        # Crea la lista con Treeview
        self.lista_clientes = ttk.Treeview(self.Fr_Principal, height=50, columns=("ID", "Nombre", "Apellido", "DNI", "Email", "Telefono", "Editar", "Eliminar"), show="headings")
        self.lista_clientes.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.3)

        self.actualizar_listado_al_iniciar()
        
        self.lista_clientes.bind("<Button-1>", self.detectar_seleccion)

        style.configure("Treeview.Heading", font=("Carme", 14))
        style.configure("Treeview.Heading", padding=3)

        style.configure("Treeview", font=("Carme", 14))
        style.configure("Treeview", rowheight=30)

        # Configura el nombre de las columnas
        self.lista_clientes.heading("ID", text="ID")
        self.lista_clientes.heading("Nombre", text="Nombre")
        self.lista_clientes.heading("Apellido", text="Apellido")
        self.lista_clientes.heading("DNI", text="DNI")
        self.lista_clientes.heading("Email", text="Email")
        self.lista_clientes.heading("Telefono", text="Telefono")
        self.lista_clientes.heading("Editar", text="Editar")
        self.lista_clientes.heading("Eliminar", text="Eliminar")

        # Configura las columnas
        self.lista_clientes.column("ID", width=25, anchor="center",stretch=True)
        self.lista_clientes.column("Nombre", width=100, anchor="center",stretch=True)
        self.lista_clientes.column("Apellido", width=100, anchor="center",stretch=True)
        self.lista_clientes.column("DNI", width=75, anchor="center",stretch=True)
        self.lista_clientes.column("Email", width=200, anchor="center",stretch=True)
        self.lista_clientes.column("Telefono", width=100, anchor="center",stretch=True)
        self.lista_clientes.column("Editar", width=50, anchor="center",stretch=True)
        self.lista_clientes.column("Eliminar", width=65, anchor="center",stretch=True)

        #self.lista_clientes.insert("", "end", values=("9999", "Santiago Nahuel", "Barrionuevo", "12.345.678", "santiagobarrionuevo391@gmail.com", "12 3456-7890", "Editar", "Eliminar"))

        # BOTONES

        # Boton de registrar cliente

        btn_reg_cli = Button(self.Fr_Principal, text=ph_registrar_cliente, font=("Carme", 16), command=self.menu_registrar_cliente)
        btn_reg_cli.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.06)

    def menu_registrar_cliente(self):

        self.ventana_menu = ctk.CTkToplevel(self.ventana)
        self.ventana_menu.title("Registrar Cliente")
        self.ventana_menu.geometry("350x300")

        # Evitar que se pueda redimensionar
        self.ventana_menu.resizable(False, False)
        self.ventana_menu.grab_set()

        # Frame
        Fr_Ventana = Frame(self.ventana_menu, background="#fdfdfd")
        Fr_Ventana.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ENTRYS Y LABELS

        # Nombre: Label
        self.lbl_Nombre = Label(Fr_Ventana,
                                text=ph_nombre_singular,
                                font=("Carme", 14),
                                anchor="w",
                                background="#fdfdfd"
                                )
        
        self.lbl_Nombre.place(relx=0.1, rely=0.1, relwidth=0.4, relheight=0.06)

        # Nombre: Entry
        self.ent_Nombre = Entry(Fr_Ventana, font=("Carme", 14),validate="key",validatecommand=self.limitar_letras_espacios)
        self.ent_Nombre.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.06)
        
        self.ent_Nombre.bind("<FocusOut>", lambda e: self.formatear_entry(e, self.ent_Nombre))

        # Apellido: Label
        self.lbl_Apellido = Label(Fr_Ventana,
                                  text=ph_apellido,
                                  font=("Carme", 14),
                                  anchor="w",
                                  background="#fdfdfd"
                                  )
        
        self.lbl_Apellido.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.06)

        # Apellido: Entry
        self.ent_Apellido = Entry(Fr_Ventana, font=("Carme", 14),validate="key",validatecommand=self.limitar_letras_espacios)
        self.ent_Apellido.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.06)
        
        self.ent_Apellido.bind("<FocusOut>", lambda e: self.formatear_entry(e, self.ent_Apellido))

        # DNI: Label
        self.lbl_DNI = Label(Fr_Ventana, text="DNI",
                             font=("Carme", 14),
                             anchor="w",
                             background="#fdfdfd"
                             )
        
        self.lbl_DNI.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.06)

        # DNI: Entry
        self.ent_DNI = Entry(Fr_Ventana, font=("Carme", 14),validate="key",validatecommand=self.limitar_numeros)
        self.ent_DNI.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.06)

        # Email: Label
        self.lbl_Email = Label(Fr_Ventana,
                               text=ph_correo,
                               font=("Carme", 14),
                               anchor="w",
                               background="#fdfdfd"
                               )
        
        self.lbl_Email.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.06)

        # Email: Entry
        self.ent_Email = Entry(Fr_Ventana, font=("Carme", 14),validate="key",validatecommand=self.validar_correo)
        self.ent_Email.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.06)

        # Telefono: Label
        self.lbl_Telefono = Label(Fr_Ventana, text="Telefono", font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_Telefono.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.06)

        # Telefono: Entry
        self.ent_Telefono = Entry(Fr_Ventana, font=("Carme", 14),validate="key",validatecommand=self.limitar_numeros)
        self.ent_Telefono.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.06)

        # Boton Confirmar

        self.btn_Conf = Button(Fr_Ventana, text=ph_confirmar, font=("Carme", 14), command=self.registrar_cliente)
        self.btn_Conf.place(relx=0.6, rely=0.85, relwidth=0.2, relheight=0.1)

        # .Binds

        self.ent_Nombre.bind("<Return>", lambda e: self.ent_Apellido.focus_set())
        self.ent_Apellido.bind("<Return>", lambda e:self.ent_DNI.focus_set())
        self.ent_DNI.bind("<Return>", lambda e: self.ent_Email.focus_set())
        self.ent_Email.bind("<Return>", lambda e: self.ent_Telefono.focus_set())
        self.ent_Telefono.bind("<Return>", lambda e: self.registrar_cliente())
    
    def menu_editar_cliente(self, event):

        self.cliente = self.lista_clientes.identify_row(event.y)
        self.valores = self.lista_clientes.item(self.cliente, "values")

        self.bd.cursor.execute(""" SELECT * FROM clientes WHERE id = ? """, (self.valores[0],))

        self.ventana_menu = ctk.CTkToplevel(self.ventana)
        self.ventana_menu.title(f"Editar Cliente con ID: {self.valores[0]}")
        self.ventana_menu.geometry("350x300")

        # Evitar que se pueda redimensionar
        self.ventana_menu.resizable(False, False)
        self.ventana_menu.grab_set()

        # Frame
        Fr_Ventana = Frame(self.ventana_menu, background="#fdfdfd")
        Fr_Ventana.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ENTRYS Y LABELS

        # Nombre: Label
        self.lbl_Nombre = Label(Fr_Ventana, text=ph_nombre, font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_Nombre.place(relx=0.1, rely=0.1, relwidth=0.4, relheight=0.06)

        # Nombre: Entry
        self.ent_Nombre = Entry(Fr_Ventana, font=("Carme", 14))
        self.ent_Nombre.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.06)

        # Apellido: Label
        self.lbl_Apellido = Label(Fr_Ventana, text=ph_apellido, font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_Apellido.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.06)

        # Apellido: Entry
        self.ent_Apellido = Entry(Fr_Ventana, font=("Carme", 14))
        self.ent_Apellido.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.06)

        # DNI: Label
        self.lbl_DNI = Label(Fr_Ventana, text="DNI", font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_DNI.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.06)

        # DNI: Entry
        self.ent_DNI = Entry(Fr_Ventana, font=("Carme", 14))
        self.ent_DNI.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.06)

        # Email: Label
        self.lbl_Email = Label(Fr_Ventana, text=ph_correo, font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_Email.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.06)

        # Email: Entry
        self.ent_Email = Entry(Fr_Ventana, font=("Carme", 14))
        self.ent_Email.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.06)

        # Telefono: Label
        self.lbl_Telefono = Label(Fr_Ventana, text="Telefono", font=("Carme", 14), anchor="w", background="#fdfdfd")
        self.lbl_Telefono.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.06)

        # Telefono: Entry
        self.ent_Telefono = Entry(Fr_Ventana, font=("Carme", 14))
        self.ent_Telefono.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.06)

        # Boton Confirmar

        self.btn_Conf = Button(Fr_Ventana, text=ph_guardar, font=("Carme", 14), command=lambda:self.actualizar_cliente(event))
        self.btn_Conf.place(relx=0.6, rely=0.85, relwidth=0.2, relheight=0.1)

        # .Binds

        self.ent_Nombre.bind("<Return>", lambda e: self.ent_Apellido.focus_set())
        self.ent_Apellido.bind("<Return>", lambda e:self.ent_DNI.focus_set())
        self.ent_DNI.bind("<Return>", lambda e: self.ent_Email.focus_set())
        self.ent_Email.bind("<Return>", lambda e: self.ent_Telefono.focus_set())
        self.ent_Telefono.bind("<Return>", lambda e: self.actualizar_cliente(event))

        self.ent_Nombre.insert(0, self.valores[1])
        self.ent_Apellido.insert(0, self.valores[2])
        self.ent_DNI.insert(0, self.valores[3])
        self.ent_Email.insert(0, self.valores[4])
        self.ent_Telefono.insert(0, self.valores[5])

    def registrar_cliente(self):

        nombre = self.ent_Nombre.get()
        apellido = self.ent_Apellido.get()
        dni = self.ent_DNI.get()
        email = self.ent_Email.get()
        telefono = self.ent_Telefono.get()

        if not nombre and not apellido and not dni and not email and not telefono:

            ms.showerror("Error!", "Ninguna de las casillas puede estar vacia.", parent=self.ventana_menu)
            return
            
        if not nombre:

            ms.showerror("Error!", "La casilla de Nombre no puede estar vacia.", parent=self.ventana_menu)
            return

        if not apellido:

            ms.showerror("Error!", "La casilla de Apellido no puede estar vacia.", parent=self.ventana_menu)
            return
        
        if not dni:

            ms.showerror("Error!", "La casilla de DNI no puede estar vacia.", parent=self.ventana_menu)
            return
        
        if not email:

            ms.showerror("Error!", "La casilla de Email no puede estar vacia.", parent=self.ventana_menu)
            return
        
        if not telefono:

            ms.showerror("Error!", "La casilla de Telefono no puede estar vacia.", parent=self.ventana_menu)
            return
        
        if nombre and apellido and dni and email and telefono:

            query = """ INSERT INTO clientes (nombre, apellido, dni, email, telefono) VALUES (?, ?, ?, ?, ?)"""
            data = (nombre, apellido, dni, email, telefono)
            
            self.bd.cursor.execute(query, data)
            self.bd.conexion.commit()

            self.actualizar_listado()

            ms.showinfo("Listo!", "Cliente registrado exitosamente.", parent=self.ventana)
            return
    
    def actualizar_cliente(self, event):

        self.cliente = self.lista_clientes.identify_row(event.y)
        self.valores = self.lista_clientes.item(self.cliente, "values")

        self.nombre = self.ent_Nombre.get()
        self.apellido = self.ent_Apellido.get()
        self.dni = self.ent_DNI.get()
        self.email = self.ent_Email.get()
        self.telefono = self.ent_Telefono.get()

        query = """ UPDATE clientes SET nombre = ?, apellido = ?, dni = ?, email = ?, telefono = ? WHERE id = ? """
        data = (self.nombre, self.apellido, self.dni, self.email, self.telefono, self.valores[0])

        self.bd.cursor.execute(query, data)
        self.bd.conexion.commit()
        
        self.ventana_menu.destroy()
        self.actualizar_listado_al_iniciar()

        ms.showinfo("Listo!", "Cliente actualizado exitosamente.", parent=self.ventana)

    def eliminar_cliente(self, event):

        self.cliente = self.lista_clientes.identify_row(event.y)
        self.valores = self.lista_clientes.item(self.cliente, "values")

        query = """ DELETE FROM clientes WHERE id = ? """
        data = (self.valores[0],)

        self.bd.cursor.execute(query, data)
        self.bd.conexion.commit()

        self.actualizar_listado_al_iniciar()
    
    def actualizar_listado(self):

        # Limpia la lista
        for cliente in self.lista_clientes.get_children():

            self.lista_clientes.delete(cliente)

        # Solicita los datos de la tabla
        self.bd.cursor.execute(""" SELECT * FROM clientes """)

        clientes_registrados = self.bd.cursor.fetchall()

        for cliente in clientes_registrados:

            self.lista_clientes.insert("", "end", values=(cliente[0],
                                                          cliente[1],
                                                          cliente[2],
                                                          cliente[3],
                                                          cliente[4],
                                                          cliente[5],
                                                          "Editar",
                                                          "Eliminar"))
        
        # Cierra la ventana para ingresar datos
        self.ventana_menu.destroy()

    def actualizar_listado_al_iniciar(self):

        # Limpia la lista
        for cliente in self.lista_clientes.get_children():

            self.lista_clientes.delete(cliente)
        
        # Solicita los datos de la tabla
        self.bd.cursor.execute(""" SELECT * FROM clientes """)

        clientes_registrados = self.bd.cursor.fetchall()

        for cliente in clientes_registrados:

            self.lista_clientes.insert("", "end", values=(cliente[0],
                                                          cliente[1],
                                                          cliente[2],
                                                          cliente[3],
                                                          cliente[4],
                                                          cliente[5],
                                                          "Editar",
                                                          "Eliminar"))
        
    def detectar_seleccion(self, event):

        self.cliente = self.lista_clientes.identify_row(event.y)
        self.columna = self.lista_clientes.identify_column(event.x)

        if not self.cliente:

            return

        self.valores = self.lista_clientes.item(self.cliente, "values")

        if self.columna == "#7":

            self.menu_editar_cliente(event)

        if self.columna == "#8":

            respuesta = ms.askyesno("Aviso!", f"Desea eliminar el cliente con ID {self.valores[0]}?", parent=self.ventana)
            
            if respuesta:
                
                self.eliminar_cliente(event)
