import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class HistorialPagos:
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def connect_to_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="undac",
            database="mineria_db"
        )

    def fetch_payments(self):
        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()
            query = """
            SELECT p.id, e.nombre, p.monto, p.fecha
            FROM pagos p
            JOIN empleados e ON p.empleado_id = e.id
            """
            cursor.execute(query)
            payments = cursor.fetchall()
            return payments
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al recuperar pagos: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def create_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Historial de Pagos")
        
        # Crear la tabla de pagos
        columns = ("id", "nombre", "monto", "fecha")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos de pagos
        payments = self.fetch_payments()
        for pay in payments:
            self.tree.insert("", tk.END, values=pay)
        
        # Configurar el layout
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

