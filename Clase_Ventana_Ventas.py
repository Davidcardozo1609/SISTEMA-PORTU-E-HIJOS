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

#OTROS
import sys, os

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
        
        self.ventana.title ("Ventas")
        self.validar = self.ventana.register (self.nunu)
        
        self.Lbl_nombre_modulo.configure(text="Ventas")
        
        
        self.soyunboton = ctk.CTkButton (self.ventana, text = "soy.un.boton.que.abre.una.ventana",  fg_color="blue",hover_color="#00008B", command =  self.menu_ventas)
        self.soyunboton.place (relx = 0.3, rely = 0.2, relwidth = 0.2, relheight = 0.1)
        
#         frame inutil, solo sirve para testeo.
        self.frame_recibo = ctk.CTkFrame (self.ventana)
        self.frame_recibo.place (relx = 0.3, rely = 0.3, relheight = 0.5, relwidth = 0.6)
          #         treeview
        self.mlem = ttk.Treeview (self.frame_recibo)
        self.mlem["column"] = ( "producto", "cantidad", "precio", "tipo de pago", "pago","id")
        
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
    
        
        
        
        self.mlem.heading ("producto",  text = "producto", anchor = tk.W)
        self.mlem.heading ("cantidad", text = "cantidad", anchor = tk.CENTER)
        self.mlem.heading ("precio", text = "precio", anchor = tk.CENTER)
        self.mlem.heading ("tipo de pago", text="tipo de pago", anchor = tk.E)
        self.mlem.heading ("pago", text = "pago", anchor = tk.E)
        self.boton_añadir_bd = ctk.CTkButton (self.ventana, text = "usame.paraañadir.datosa.la.bd",  fg_color="blue",hover_color="#00008B",command = lambda: self.añadir_datos_bd())
        self.boton_añadir_bd.place (relx = 0.3, rely = 0.8, relwidth = 0.1, relheight = 0.1)
        
        
    def nunu (self,er):
       return er.isdigit() or er==""
    
        
        
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
                                              values = self.filas,
                                              font = ("Carme", 16),
                                              command = self.mostrar_cantidad)
        self.menu_opcion.place (relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)
        
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

        self.boton_añadir = ctk.CTkButton (self.er, text = ("soy.un.boton.que...roba.datos.v3"), font = ("Carme", 16), command = lambda: self.robar_datos())
        self.boton_añadir.place (relx = 0.1, rely = 0.7, relwidth = 0.8, relheight = 0.1)
        ml = self.opcion_metodo_pago.get()
        print (ml)
      
#   Somos.lasfuncionesysolohacemossufrir alquenosuse.
    def robar_datos(self):
     
        
        producto = self.menu_opcion.get()
        cantidad = self.cantidad_opcion.get()
        
        precio = self.entry_precio.get()
        tipo_pago = self.opcion_metodo_pago.get()
        pago = int(cantidad) * int(precio)
        print (producto)
        print (cantidad)
        print (precio)
        print (tipo_pago)
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
        
        
       
        
            
            
            
            

        if producto ==  self.mle[0]:
            ms.showerror("Repeticion","producto ya colocado", parent = self.er)
            return
        query = ("""SELECT cantidad FROM productos_stock WHERE producto =  ?""")
        data = (producto,)
        consulta1 = self.bd.cursor.fetchone()[0]
        consulta_int = int(consulta1)
        self.bd.cursor.execute(query,data)
        
      
        if int(cantidad)>consulta_int:
            ms.showerror ("error""La cantidad que haz intentado colocar es mayor que la cantidad actual")
            return
        
        if not cantidad:
            ms.showerror ("Faltante", "Falta colocar la cantidad")
            return
        elif not precio:
            ms.showerror ("Faltante", "Falta colocar el precio")
            return
    
        
     
        self.cantidad_opcion.delete(0, "end")
        self.entry_precio.delete(0, "end")
        ms.showinfo ("feli", "feli", parent = self.er)
        
        query = ("""SELECT id FROM productos_stock WHERE producto = ?""")
        data = (producto,)
        self.bd.cursor.execute(query,data)
        idd = self.bd.cursor.fetchone()[0]
        print (idd)
      
        self.mlem.insert("", tk.END, values = (producto, cantidad, precio, tipo_pago, pago, idd))
        
        self.mlem.pack (fill="both", expand = True)
       
        
       
            
        
        
        
    def mostrar_cantidad(self,producto):
       
            
           
       
        
            self.cantidad_bd = ctk.CTkLabel (self.er, text = "", font = ("Carme", 10))
            self.cantidad_bd.place (relx = 0.7, rely = 0.2, relwidth = 0.25, relheight = 0.05)
            query = ("""SELECT cantidad FROM productos_stock WHERE producto = ?""")
            data = ((producto),)
            self.prueba = self.bd.cursor.fetchone()
            self.bd.cursor.execute(query,data)
            
            print (self.prueba)
            
            self.cantidad_bd.configure (text = self.prueba)
    def añadir_datos_bd(self):
         self.listae = []
         for mlemem in self.mlem.get_children():
            self.valor = self.mlem.item(mlemem,"values")
            print(self.valor)
            lista = {
                "producto": self.valor[0],
                "cantidad":self.valor[1],
                "precio": self.valor[2],
                "tipo de pago": self.valor[3],
                "pago": self.valor[4],
                "id": self.valor[5]
                }
            self.listae.append(lista)
            query = ("""SELECT cantidad FROM productos_stock WHERE producto = ? """)
            data= (self.valor[0],)
            
            self.bd.cursor.execute(query,data)
            mleem = self.bd.cursor.fetchone()[0]
            
            
            mamayo =  int(mleem)-int(self.valor[1])
            print ("como.siempre.soy.un.print.inutil", mamayo)
                                                                               
            self.bd.cursor.execute ("""
                    
                    
            INSERT INTO ventas (productos, cantidad, precio, tipo_pago, pago) VALUES (?,?,?,?,?)
                        
            """, (self.valor[0], self.valor[1], self.valor[2], self.valor[3], self.valor[4]))
            
        
            
           
                
                 
            
                  
            self.bd.cursor.execute("""
            UPDATE productos_stock SET cantidad = ? WHERE id = ?""",
            (mamayo, self.valor[5]))
            if mamayo == 0:
                
                self.bd.cursor.execute("""
                DELETE FROM productos_stock WHERE cantidad = ?""",(mamayo,))
            
        
         self.bd.conexion.commit()
                                               
                        
                        
                        
         ms.showinfo ("felicidades", "Haz compretado la venta", parent = self.ventana)
            
         for e in self.mlem.get_children():
                         self.mlem.delete(e)

                        
                
                
            
