#____________LIBRERIAS_________________#

#INTERFAZ
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox as ms
import customtkinter as ctk

#CLASES
from Constantes import *
from bd import BaseDeDatos
from Plantilla import Clase_Plantilla
from Clase_Gestor_Ventanas import GestorVentanas
from Clase_Ventana_Stock import Productos

#OTROS
import sys, os
from datetime import datetime

#_________________________________CLASE VENTAS_____________________________________________#
class Ventas(Clase_Plantilla):
    def __init__(self,master, titulo="hollaaa",ventana_padre=None,ventana_login=None, usuario_actual=None,parent_app=None):
        # Llamamos al constructor de Stock con sus parámetros
        super().__init__(master=master,
                 titulo=titulo,
                 ventana_padre=ventana_padre,
                 ventana_login=ventana_login,
                 usuario_actual=usuario_actual,
                 parent_app=parent_app)
        
        self.bd = BaseDeDatos()

        self.ventana_padre=ventana_padre
        
        self.ventana.title ("Ventas")


        self.validar = self.ventana.register (self.nunu)
        self.validar2 = self.ventana.register (self.nunu2)
        
        self.Lbl_nombre_modulo.configure(font=("Segoe UI", 50, "bold"),text="Ventas")
        self.Lbl_nombre_modulo.place(relx=0.05,rely=0.03,relwidth=0.382,relheight=0.1)
        
        
        self.soyunboton = ctk.CTkButton (self.ventana, text = "+ Añadir producto",  fg_color="blue",hover_color="#00008B",  font = ("Carme", 18), command =  self.menu_ventas)
        self.soyunboton.place (relx = 0.3, rely = 0.22, relwidth = 0.13, relheight = 0.06)
        
#         frame inutil, solo sirve para testeo.
        self.frame_recibo = ctk.CTkFrame (self.ventana)
        self.frame_recibo.place (relx = 0.3, rely = 0.31, relheight = 0.47, relwidth = 0.6)
          #         treeview
        self.mlem = ttk.Treeview (self.frame_recibo)
        self.mlem["column"] = ( "producto", "cantidad", "precio", "tipo de pago", "pago","id", "editar", "eliminar")
        
        #Che tomi hay una funcion que vos le pasas los encabezados y los datos y te crea la tabla xd
        #Hola.comentario.dearriba.Lamento.informartequeyo.no.voyahacer.eso.Porfavor.matese.
        
        
        
        self.mlem.pack (fill="both", expand = True)
        self.mlem.column ("#0", width = 0, stretch="no")
      
        self.mlem.column ("producto", width = 25, anchor=tk.W)
        self.mlem.column ("cantidad", width = 25, anchor = tk.CENTER)
        self.mlem.column ("precio", width = 25, anchor = tk.CENTER)
        self.mlem.column ("tipo de pago", width = 25, anchor = tk.E)
        self.mlem.column ("pago", width = 25, anchor = tk.E)
        self.mlem.column ("id", width = 0, stretch = "no")
        self.mlem.column ("editar", width = 5, anchor = tk.E)
        self.mlem.column ("eliminar", width = 5, anchor = tk.E)
    
        
        
        
        self.mlem.heading ("producto",  text = "producto", anchor = tk.W)
        self.mlem.heading ("cantidad", text = "cantidad", anchor = tk.CENTER)
        self.mlem.heading ("precio", text = "precio", anchor = tk.CENTER)
        self.mlem.heading ("tipo de pago", text="tipo de pago", anchor = tk.E)
        self.mlem.heading ("pago", text = "Total", anchor = tk.E)
        self.mlem.heading ("editar", text = "Editar", anchor = tk.E)
        self.mlem.heading ("eliminar", text = "eliminar", anchor = tk.E)
        
        self.boton_añadir_bd = ctk.CTkButton (self.ventana, text = "Finalizar venta",  fg_color="blue",hover_color="#00008B", font = ("Carme", 16),command = lambda: self.añadir_datos_bd())
        self.boton_añadir_bd.place (relx = 0.3, rely = 0.8, relwidth = 0.1, relheight = 0.1)
        self.mlem.bind ("<Button-1>", self.editar_arbolito)
        
        
    def nunu (self,er):
       
        return (
        er == "" or
        (len(er) <= 10 and
         er.replace(".", "", 1).isdigit())
        )
    def nunu2 (self,er):
        if len(er)<5:
            return er.isdigit() or er == ""
        else:
            return er == ""
    
        
        
    def menu_ventas(self):
            
        self.er = ctk.CTkToplevel(self.ventana)
        
        self.er.geometry ('250x250')
#         Trata.bien.a.la.sub.ventana.ella.nacio.hace.poco.
        self.er.title ("soy.una.sub.ventana.tratame.bien.")
        self.er.grab_set()
        query = ("""SELECT producto FROM productos_stock""")
        self.bd.cursor.execute(query)
        self.mle = self.bd.cursor.fetchall()
        self.filas = [fila[0] for fila in self.mle]
        print (self.mle)
        self.menu_opcion = ctk.CTkOptionMenu (self.er,
                                              values =  ([""]) +list(self.filas),
                                              font = ("Carme", 16),
                                              command = self.mostrar_cantidad)
        self.menu_opcion.place (relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)
        self.cantidad_bd = ctk.CTkLabel (self.er, text = "", font = ("Carme", 10))
        self.cantidad_bd.place (relx = 0.7, rely = 0.2, relwidth = 0.25, relheight = 0.05)
        self.cantidad_bd_consiguio = self.menu_opcion.get()
        self.producto_label = ctk.CTkLabel (self.er, text = "Producto:", font = ("Carme", 10))
        self.producto_label.place (relx = 0.08, rely = 0.05, relwidth = 0.25, relheight = 0.05)
        
        
    
        
        self.cantidad_opcion = ctk.CTkEntry (self.er,  validate="key", validatecommand=(self.validar, "%P"))
        self.cantidad_opcion.place (relx = 0.1, rely =0.25, relwidth = 0.8, relheight = 0.1)
        
        
        self.cantidad_label = ctk.CTkLabel (self.er, text = "Cantidad:", font = ("Carme", 10))
        self.cantidad_label.place (relx = 0.08, rely = 0.2, relwidth = 0.25, relheight = 0.05)
        
        
        self.precio_label = ctk.CTkLabel (self.er, text = "Precio:", font = ("Carme", 10))
        
        self.precio_label.place (relx = 0.05, rely = 0.35, relwidth = 0.25, relheight = 0.05)
        self.entry_precio = ctk.CTkEntry (self.er,validate="key", validatecommand=(self.validar, "%P"))
        self.entry_precio.place (relx = 0.1, rely = 0.4, relwidth = 0.8, relheight = 0.1)
        self.label_metodopago=ctk.CTkLabel (self.er, text = "Metodo de pago:", font = ("Carme", 10))
        self.label_metodopago.place (relx = 0.05, rely= 0.5, relwidth = 0.35, relheight = 0.05)
        self.opcion_metodo_pago = ctk.CTkOptionMenu (self.er,
                                                     font = ("Carme", 16),
                                                     values = ["Efectivo", "Transferencia", "Credito", "Debito"],
                                                     
                                                     )
        self.opcion_metodo_pago.place (relx = 0.1, rely = 0.55, relwidth = 0.8, relheight = 0.1)

        self.boton_añadir = ctk.CTkButton (self.er, text = ("Finalizar"), font = ("Carme", 16), command = lambda: self.robar_datos())
        self.boton_añadir.place (relx = 0.1, rely = 0.7, relwidth = 0.8, relheight = 0.05)
        self.cantidad_opcion.bind ("<Return>", lambda e: self.entry_precio.focus())
        self.entry_precio.bind ("<Return>", lambda e: self.boton_añadir.focus())
        self.boton_añadir.bind ("<Return>", lambda e: self.robar_datos())
        
      
#   Somos.lasfuncionesysolohacemossufrir alquenosuse.
    def robar_datos(self):
     
        
        productoo = self.menu_opcion.get()
        cantidad = self.cantidad_opcion.get()

        if not productoo:
            ms.showerror ("Faltante", "Falta colocar un producto")
            return


        if not cantidad:
            ms.showerror ("Faltante", "Falta colocar la cantidad")
            return
        
        precio = self.entry_precio.get()
        if not precio:
            ms.showerror ("Faltante", "Falta colocar el precio")
            return
    
        tipo_pago = self.opcion_metodo_pago.get()
        
        pago = int(cantidad) * int(precio)

        self.lista_mlem =[]
        for fila in self.mlem.get_children():
            self.mle = self.mlem.item (fila,"values")
            self.li = {
               
                "producto": self.mle[0],
                "cantidad":self.mle[1],
                "precio": self.mle[2],
                "tipo de pago": self.mle[3],
                "pago": self.mle[4]
                
               
                
                }
        
            self.lista_mlem.append(self.li)
        
            

        if productoo ==  self.mle[0]:
            ms.showerror("Repeticion","producto ya colocado", parent = self.er)
            return
        query = ("""SELECT cantidad FROM productos_stock WHERE producto =  ?""")
        data = (productoo,)
       
        self.bd.cursor.execute(query,data)
        consulta1 = self.bd.cursor.fetchone() [0]
       
        consulta_int = int(consulta1)
        
      
        if int(cantidad)>consulta_int:
            ms.showerror ("error", "La cantidad que haz intentado colocar es mayor que la cantidad actual")
            return
     
        self.cantidad_opcion.delete(0, "end")
        self.entry_precio.delete(0, "end")

        ms.showinfo ("Felicidades", "Los datos han sido añadidos correctamente.", parent = self.er)
        
        query = ("""SELECT id FROM productos_stock WHERE producto = ?""")
        data = (productoo,)
        self.bd.cursor.execute(query,data)
        self.idd = self.bd.cursor.fetchone()[0]

      
        self.mlem.insert("", tk.END, values = (productoo, cantidad, precio, tipo_pago, pago, self.idd,"editar", "eliminar"))
        
        self.mlem.pack (fill="both", expand = True)
       
        
       
            
        
        
        
    def mostrar_cantidad(self,producto):
            ml = self.menu_opcion.get()
            query = ("""SELECT cantidad FROM productos_stock WHERE producto = ?""")
            data = (ml,)
            
            self.bd.cursor.execute(query,data)
            self.prueba = self.bd.cursor.fetchone()
            self.cantidad_bd = ctk.CTkLabel (self.er, text = "", font = ("Carme", 10))
            self.cantidad_bd.place (relx = 0.7, rely = 0.2, relwidth = 0.25, relheight = 0.05)
            self.cantidad_bd.configure (text = self.prueba)


            
           
            
    def editar_arbolito(self,event):
        x, y = event.x, event.y
        self.editar_datos = self.mlem.identify_row(y)
        self.editar_datoss = self.mlem.identify_column (x)
  
        
        
        if self.editar_datoss == "#7" and self.editar_datos :
            print ("Mi.segundo.nombre.va.ser.aubree.no.aubrey") #Esteprint.nolo.borro.para.confundir.y.porque.si.No.me.preguntres.que.significa.
            self.subventana = ctk.CTkToplevel (self.ventana)
            self.subventana.geometry = ('250x250')
            self.subventana.title  ("Editar")
            self.subventana.grab_set()
            
            self.err = self.mlem.item(self.editar_datos,"values")
            self.mlm = {
                "producto": self.err[0],
                "cantidad": self.err[1],
                "precio": self.err[2]
                }
            
            
            
           
            query = ("""SELECT producto FROM productos_stock""")
            
            
            self.bd.cursor.execute(query)
            mleem = self.bd.cursor.fetchall()
            self.menu_la = ctk.CTkLabel (self.subventana, text = "Producto", font = ("Carme", 10))
            self.menu_la.place (relx = 0.1, rely = 0.05, relheight = 0.5, relwidth = 0.22)
            self.menu_v2 = ctk.CTkOptionMenu (self.subventana,
                                                             values =[self.err[0]]+list(self.filas),
                                                             font = ("Carme", 16),
                                                             command = self.mostrar_cantidad2)
            self.menu_v2.place (relx = 0.1, rely = 0.1, relheight = 0.1, relwidth = 0.85)
            
            
            self.cantidad_label = ctk.CTkLabel (self.subventana, font = ("Carme", 10), text = "Cantidad")
            self.cantidad_label.place (relx = 0.11, rely = 0.20, relheight = 0.05, relwidth = 0.22)
            
            self.label_cantidad_bd = ctk.CTkLabel (self.subventana, text = "", font = ("Carme", 10))
            self.label_cantidad_bd.place (relx = 0.8, rely = 0.20, relheight = 0.05, relwidth = 0.22)
            
            
            
            self.cantidad_entry = ctk.CTkEntry(self.subventana, validate = "key",  validatecommand=(self.validar2, "%P"), font =("Carme", 16))
            self.cantidad_entry.place (relx = 0.1, rely = 0.25, relheight = 0.1, relwidth = 0.85)
            self.cantidad_entry.insert (0,self.err[1])
            
            self.precio_label = ctk.CTkLabel (self.subventana, font = ("Carme", 10), text = "Precio")
            self.precio_label.place (relx = 0.085, rely = 0.35, relheight = 0.05, relwidth = 0.22)
            
            self.precio_entry  = ctk.CTkEntry (self.subventana, font = ("Carme", 16), validate = "key",  validatecommand=(self.validar, "%P"))
            self.precio_entry.place (relx = 0.1, rely = 0.40, relheight = 0.1, relwidth = 0.85)
            self.precio_entry.insert (0,self.err[2])
            
            self.metododepagolabel = ctk.CTkLabel (self.subventana, text = "Metodo de pago", font = ("Carme", 10))
            self.metododepagolabel.place (relx = 0.085, rely = 0.50, relheight = 0.05, relwidth = 0.42)
            
            self.metododepago2 =ctk.CTkOptionMenu (self.subventana,
                                                                                        values =  ["Efectivo", "Transferencia", "Credito", "Debito"],
                                                                                        font = ("Carmen", 16))
            self.metododepago2.place (relx = 0.1, rely = 0.55, relheight = 0.1, relwidth = 0.85)
            
            self.boton_finalizar = ctk.CTkButton (self.subventana, text = "Finalizar", command = lambda: self.actualizar())
            self.boton_finalizar.place (relx = 0.1, rely = 0.7, relheight = 0.1, relwidth = 0.85)
            self.cantidad_entry.bind ("<Return>", lambda e: self.precio_entry.focus())
            self.precio_entry.bind ("<Return>", lambda e: self.boton_finalizar.focus())
            self.boton_finalizar.bind ("<Return>", lambda e: self.actualizar())
        elif self.editar_datoss == "#8" and self.editar_datos:
            er = ms.askquestion ("Eliminar fila?", "Enserio quieres eliminar esta fila?", parent = self.ventana)
            if er == "yes":
                self.mlem.delete(self.editar_datos)
                ms.showinfo ("Realizado", "Se ha eliminado la fila", parent = self.ventana)
            else:
                ms.showinfo ("Decision","No se ha eliminado la fila", parent = self.ventana)
            
            
            #Holaaa,soy.lapersonaqueha.progamado.esto.Paraavisarte.que.odio.mi.vida.Porfavor.haganque.si.escucho.your.problem.me.de.underrame.cerebral.asi.dejodeprogamar.
                                                                                       
            
            
    def actualizar(self):

        actupro = self.menu_v2.get()
        actucan = self.cantidad_entry.get()



        if not actucan:
            ms.showwarning ("Error", "No haz colocado una cantidad a actualizar", parent = self.subventana)
            self.actucan.delete (0,"end")
            self.actuprec.delete (0,"end")
            return
        

        actuprec = self.precio_entry.get()


        if not actuprec:
            ms.showwarning ("Error", "No haz colocado un precio a actualizar", parent = self.subventana)
            self.actucan.delete (0,"end")
            self.actupro.delete (0,"end")
            return
        

        for fila in self.mlem.get_children():
            self.mler = self.mlem.item (fila,"values")
            lim ={
                "producto": self.mler[0]
                }
            actutipopago = self.metododepago2.get()
        
        
        
            if self.editar_datos == fila:
                continue
            #chatgptafullcon lodel.mlemitem


            if actupro == self.mler[0] :
                ms.showwarning ("error", "No se puede realizar la operacion", parent = self.subventana)
                return
        
        query = ("""SELECT cantidad FROM productos_stock WHERE producto =  ?""")
        data = (actupro,)
       
        self.bd.cursor.execute(query,data)
        consulta2 = self.bd.cursor.fetchone() [0]
       
        consulta_int2 = int(consulta2)
        
        if int(actucan)>int(consulta2):
            ms.showwarning ("Error", "La cantidad que se ha ingresado es mayor que la cantidad disponible", parent = self.subventana)
            return
        
        
        
        totalnuevo = int(actucan) * float(actuprec)
        self.mlem.delete(self.editar_datos)
       
        self.mlem.insert ("", tk.END, values = (actupro, actucan, actuprec, actutipopago, totalnuevo,self.idd, "editar", "eliminar"))
        
        ms.showinfo ("Felicidades", "Haz actualizado el producto", parent = self.subventana)
        self.subventana.destroy()
    
         
        
        
        
                                                             
            
    def mostrar_cantidad2(self, producto):
        actu= self.menu_v2.get()
        query =("""SELECT cantidad FROM productos_stock WHERE producto = ?""")
        data = (actu,)
        self.bd.cursor.execute(query,data)
        err = self.bd.cursor.fetchone()
        
        self.label_cantidad_bd.configure (text = err)

        
        
    def añadir_datos_bd(self):
        self.listae = []
        total_general = 0

        # Si no hay productos en la tabla, salimos
        if not self.mlem.get_children():
            ms.showerror("Error", "No hay productos para vender", parent=self.ventana)
            return

        # 1️⃣ Creamos la venta general
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        self.bd.cursor.execute("""
            INSERT INTO registro_ventas (fecha, total)
            VALUES (?, ?)
        """, (fecha_actual, 0))  # total 0 por ahora, lo actualizamos al final

        id_venta_general = self.bd.cursor.lastrowid  # guardamos el id de la venta general

        # 2️⃣ Insertamos cada producto vendido
        for mlemem in self.mlem.get_children():
            self.valor = self.mlem.item(mlemem, "values")

            producto, cantidad, precio, tipo_pago, pago, id_producto = self.valor[:6]
            cantidad = int(cantidad)
            precio = float(precio)
            pago = float(pago)

            total_general += pago

            
            self.bd.cursor.execute("SELECT cantidad FROM productos_stock WHERE producto = ?", (producto,))
            stock_actual = self.bd.cursor.fetchone()[0]
            nuevo_stock = stock_actual - cantidad

            self.bd.cursor.execute("""
                UPDATE productos_stock SET cantidad = ? WHERE id = ?
            """, (nuevo_stock, id_producto))

            if nuevo_stock == 0:
                self.bd.cursor.execute("DELETE FROM productos_stock WHERE id = ?", (id_producto,))

            # Insertamos detalle de la venta
            self.bd.cursor.execute("""
                INSERT INTO detalle_ventas (ventas_id, productos, cantidad, precio, tipo_pago, pago)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_venta_general, producto, cantidad, precio, tipo_pago, pago))

        # 3️⃣ Actualizamos el total en la tabla principal
        self.bd.cursor.execute("""
            UPDATE registro_ventas SET total = ? WHERE id = ?
        """, (total_general, id_venta_general))

        self.bd.conexion.commit()

        self.actualizar_tabla()

        if Productos in GestorVentanas.instancias:
                GestorVentanas.instancias[Productos].actualizar_tabla()
            
        Registro_Ventas = __import__("Clase_Ventana_Registro_Ventas").Registro_Ventas

        if Registro_Ventas in GestorVentanas.instancias:
            GestorVentanas.instancias[Registro_Ventas].actualizar_tabla()

        


        ms.showinfo("Éxito", "Venta registrada correctamente", parent=self.ventana)

    def actualizar_tabla(self):
         for fila in self.mlem.get_children():
             self.mlem.delete(fila)

                        
                
                
            
