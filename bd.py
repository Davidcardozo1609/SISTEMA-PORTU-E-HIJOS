import sys, os
import sqlite3 as sqlcon
import shutil
from datetime import datetime
from tkinter import messagebox as ms

NOMBRE_DB = "mb_lenceria"

class BaseDeDatos:
    def __init__(self):
        self.ruta_bd = self.obtener_ruta_bd()
        self.conexion = sqlcon.connect(self.ruta_bd)
        self.cursor = self.conexion.cursor()
        # Solo crear tablas si la base no existe
        if not os.path.exists(self.ruta_bd):
            self.crear_bd_vacia(self.ruta_bd)


    # ----------------- Rutas -----------------
    @staticmethod
    def ruta_descargas():
        return os.path.join(os.path.expanduser("~"), "Downloads")

    # ----------------- Creación de BD -----------------
    @staticmethod
    def crear_bd_vacia(ruta):
        """Crea todas las tablas en una base de datos vacía."""
        conn = sqlcon.connect(ruta)
        cursor = conn.cursor()

        #_____________________________PROVEEDOR____________________________#

        cursor.execute("""CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL
        )""")

         #____________________________CLIENTES____________________#


        cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            dni TEXT,
            email TEXT,
            telefono TEXT
        )""")

        #_____________________________VENTAS_______________________________#

        cursor.execute("""CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productos TEXT NOT NULL,
            cantidad INT NOT NULL,
            precio INT NOT NULL,
            tipo_pago TEXT NOT NULL,
            pago INT NOT NULL
        )""")


        #_____________________________REGISTRO DE VENTAS_______________________________#
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registro_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clientes_id INTEGER NOT NULL,
                clientes TEXT NOT NULL,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (clientes_id) REFERENCES clientes(id)
            );
            """)
        
        #_____________________________DETALLES DE LA VENTA_____________________________#

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                productos TEXT NOT NULL,
                cantidad INT NOT NULL,
                precio INT NOT NULL,
                tipo_pago TEXT NOT NULL,
                subtotal INT NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES registro_ventas(id)
            );
            """)
        
        #_____________________________COMPRAS_______________________________#


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras_proveedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proveedor_id INTEGER NOT NULL,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        );
        """)

        #____________________________REGISTRO DE COMPRAS_______________________#
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registro_compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proveedor_id INTEGER NOT NULL,
                proveedor TEXT NOT NULL,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
            );
            """)
        

         #____________________________DETALLES DE LAS COMPRAS______________________#


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES registro_compras(id)
            );
            """)
        
         #____________________________EVENTOS_____________________________________#

        cursor.execute("""CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_del_evento TEXT,
            hora TEXT,
            fecha TEXT,
            descripcion TEXT
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            correo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS productos_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL
        )""")
        
        conn.commit()
        conn.close()

    # ----------------- Obtener ruta BD -----------------
    def obtener_ruta_bd(self):
        ruta_exe = os.path.abspath(NOMBRE_DB + ".db")
        carpeta_copias = os.path.join(self.ruta_descargas(), "MB_LENCERIA")
        os.makedirs(carpeta_copias, exist_ok=True)

        # 1️⃣ Si existe junto al exe, usarla
        if os.path.exists(ruta_exe):
            try:
                conn = sqlcon.connect(ruta_exe)
                conn.close()
                return ruta_exe
            except sqlcon.DatabaseError:
                os.remove(ruta_exe)

        # 2️⃣ Buscar copia válida en Descargas/MB_LENCERIA
        archivos = [f for f in os.listdir(carpeta_copias) if f.startswith(NOMBRE_DB) and f.endswith(".db")]
        archivos.sort(reverse=True)
        for archivo in archivos:
            ruta_copia = os.path.join(carpeta_copias, archivo)
            try:
                conn = sqlcon.connect(ruta_copia)
                conn.close()
                shutil.copy2(ruta_copia, ruta_exe)
                print(f"Copia restaurada desde {ruta_copia}")
                return ruta_exe
            except sqlcon.DatabaseError:
                continue

        # 3️⃣ Si no hay nada, crear BD nueva junto al exe
        self.crear_bd_vacia(ruta_exe)
        print(f"Se creó nueva base de datos en {ruta_exe}")
        return ruta_exe

    # ----------------- Guardar copia -----------------
    def guardar_copia(self):
        ruta_exe = os.path.abspath(NOMBRE_DB + ".db")
        if not os.path.exists(ruta_exe):
            ms.showerror("Error", "No hay base de datos para copiar.")
            return

        carpeta_copias = os.path.join(self.ruta_descargas(), "MB_LENCERIA")
        os.makedirs(carpeta_copias, exist_ok=True)

        nombre_copia = f"{NOMBRE_DB}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        ruta_copia = os.path.join(carpeta_copias, nombre_copia)

        try:
            shutil.copy2(ruta_exe, ruta_copia)
            ms.showinfo("Éxito", f"Copia guardada en {ruta_copia}")
        except Exception as e:
            ms.showerror("Error", f"No se pudo guardar la copia: {e}")

    # ----------------- Métodos auxiliares -----------------
    def cerrar(self):
        self.conexion.close()
