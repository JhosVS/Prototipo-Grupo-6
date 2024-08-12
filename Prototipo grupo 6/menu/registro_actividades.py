import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importar ttk para el Combobox
from tkcalendar import DateEntry
import mysql.connector
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR

class VentanaRegistroActividades(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de Actividades")
        self.geometry("400x300")
        self.config(bg=COLOR_CUERPO_PRINCIPAL)

        tk.Label(self, text="Registrar Nueva Actividad", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL).pack(pady=10)
        
        tk.Label(self, text="Nombre de la Actividad:", bg=COLOR_CUERPO_PRINCIPAL).pack(anchor='w', padx=10)
        self.nombre_actividad = tk.Entry(self)
        self.nombre_actividad.pack(fill='x', padx=10, pady=5)

        tk.Label(self, text="Fecha Límite:", bg=COLOR_CUERPO_PRINCIPAL).pack(anchor='w', padx=10)
        self.fecha_limite = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.fecha_limite.pack(fill='x', padx=10, pady=5)

        tk.Label(self, text="Estado:", bg=COLOR_CUERPO_PRINCIPAL).pack(anchor='w', padx=10)
        self.estado = ttk.Combobox(self, values=["pendiente", "cumplida"])
        self.estado.pack(fill='x', padx=10, pady=5)
        self.estado.set("pendiente")  # Valor predeterminado

        tk.Button(self, text="Guardar", command=self.guardar_actividad, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=10)

    def guardar_actividad(self):
        # Obtener los datos del formulario
        nombre = self.nombre_actividad.get()
        fecha_limite = self.fecha_limite.get_date()  # Obtener la fecha seleccionada en formato datetime
        estado = self.estado.get()  # Obtener el valor seleccionado en el Combobox

        # Convertir la fecha al formato correcto
        fecha_limite_formateada = fecha_limite.strftime("%Y-%m-%d")

        # Conectar a la base de datos MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="undac",
                database="mineria_db"
            )
            cursor = conn.cursor()
            query = """
                INSERT INTO actividades (nombre, fecha_limite, estado) 
                VALUES (%s, %s, %s)
            """
            values = (nombre, fecha_limite_formateada, estado)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Actividad registrada correctamente")
            self.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
