import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from abc import ABC, abstractmethod
import os

# Abstracción para la base de datos
class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLConnector(DatabaseConnector):
    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="undac",
            database="mineria_db"
        )

# Clase para manejar operaciones de empleados
class EmployeeRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def fetch_employees(self):
        try:
            conn = self.db_connector.connect()
            cursor = conn.cursor()
            query = "SELECT id, nombre, edad, direccion, ocupacion FROM empleados"
            cursor.execute(query)
            employees = cursor.fetchall()
            return employees
        except mysql.connector.Error as err:
            raise RuntimeError(f"Error al recuperar empleados: {err}")
        finally:
            cursor.close()
            conn.close()

# Clase para manejar operaciones de pagos
class PaymentRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def add_payment(self, employee_id, amount):
        try:
            conn = self.db_connector.connect()
            cursor = conn.cursor()
            query = "INSERT INTO pagos (empleado_id, monto, fecha) VALUES (%s, %s, CURDATE())"
            cursor.execute(query, (employee_id, amount))
            conn.commit()
        except mysql.connector.Error as err:
            raise RuntimeError(f"Error al agregar el pago: {err}")
        finally:
            cursor.close()
            conn.close()

# Clase para manejar la generación de reportes
class ReportGenerator:
    @staticmethod
    def generate_report(employee_id, employee_name, amount):
        try:
            # Asegurarse de que la carpeta de pagos exista
            os.makedirs("pagos", exist_ok=True)
            
            # Guardar el reporte en la carpeta pagos
            file_path = os.path.join("pagos", f"nomina_{employee_id}.txt")
            with open(file_path, "w") as file:
                file.write(f"Empleado: {employee_name}\n")
                file.write(f"ID del Empleado: {employee_id}\n")
                file.write(f"Monto del Pago: ${amount:.2f}\n")
            messagebox.showinfo("Éxito", "Reporte generado correctamente.")
        except IOError as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")

# Clase para la interfaz gráfica
class SistemaPagos:
    def __init__(self, parent, db_connector, employee_repo, payment_repo, report_gen):
        self.parent = parent
        self.db_connector = db_connector
        self.employee_repo = employee_repo
        self.payment_repo = payment_repo
        self.report_gen = report_gen
        self.create_window()

    def add_payment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un empleado.")
            return
        
        employee_id = self.tree.item(selected_item)["values"][0]
        employee_name = self.tree.item(selected_item)["values"][1]
        amount = simpledialog.askfloat("Monto del Pago", "Ingrese el monto a pagar:")
        
        if amount is None:
            messagebox.showerror("Error", "Debe proporcionar un monto.")
            return
        
        try:
            self.payment_repo.add_payment(employee_id, amount)
            self.report_gen.generate_report(employee_id, employee_name, amount)
            messagebox.showinfo("Éxito", "Pago agregado correctamente.")
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))

    def create_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Sistema de Pagos")
        
        columns = ("id", "nombre", "edad", "direccion", "ocupacion")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        employees = self.employee_repo.fetch_employees()
        for emp in employees:
            self.tree.insert("", tk.END, values=emp)
        
        tk.Button(self.window, text="Agregar Pago", command=self.add_payment).grid(row=1, column=0, columnspan=2, pady=10)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    db_connector = MySQLConnector()
    employee_repo = EmployeeRepository(db_connector)
    payment_repo = PaymentRepository(db_connector)
    report_gen = ReportGenerator()
    SistemaPagos(root, db_connector, employee_repo, payment_repo, report_gen)
    root.mainloop()
