import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os

class GenerarReporte(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Generar Reporte de Actividad")
        self.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
        # Crear tabla para mostrar actividades
        self.create_activity_table()

        # Entrada de descripción
        self.create_description_entry()

        # Botón para generar el reporte
        self.create_generate_report_button()

    def create_activity_table(self):
        """Crea la tabla de actividades y la carga con datos de la base de datos."""
        self.tree = ttk.Treeview(self, columns=('ID', 'Nombre', 'Fecha Límite', 'Estado'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Fecha Límite', text='Fecha Límite')
        self.tree.heading('Estado', text='Estado')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.load_activities()

    def create_description_entry(self):
        """Crea la entrada de texto para la descripción del reporte."""
        tk.Label(self, text="Descripción:").pack(pady=5)
        self.descripcion = tk.Entry(self, width=50)
        self.descripcion.pack(pady=5)

    def create_generate_report_button(self):
        """Crea el botón para generar el reporte."""
        self.generar_btn = tk.Button(self, text="Generar Reporte", command=self.generar_reporte)
        self.generar_btn.pack(pady=20)

    def load_activities(self):
        """Carga las actividades desde la base de datos en la tabla."""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="undac",
                database="mineria_db"
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, fecha_limite, estado FROM actividades;")
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    self.tree.insert('', 'end', values=row)
            else:
                print("No se encontraron actividades.")

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al conectar a la base de datos: {err}")

    def generar_reporte(self):
        """Genera el reporte basado en la actividad seleccionada y la descripción ingresada."""
        selected_item = self.tree.selection()
        if selected_item:
            actividad = self.tree.item(selected_item)['values']
            id_actividad = actividad[0]
            descripcion = self.descripcion.get()
            if descripcion:
                self.save_report(id_actividad, actividad[1], actividad[2], actividad[3], descripcion)
                self.update_activity_description(id_actividad, descripcion)
                messagebox.showinfo("Reporte", "Reporte generado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor ingrese una descripción.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione una actividad.")

    def save_report(self, id_actividad, nombre, fecha_limite, estado, descripcion):
        """Guarda el reporte en un archivo de texto en la carpeta 'reporte'."""
        if not os.path.exists('reporte'):
            os.makedirs('reporte')

        archivo_reporte = f'reporte/reporte_actividad_{id_actividad}.txt'
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write(f"Reporte de Actividad\n")
            f.write(f"---------------------\n")
            f.write(f"ID: {id_actividad}\n")
            f.write(f"Nombre: {nombre}\n")
            f.write(f"Descripción: {descripcion}\n")
            f.write(f"Fecha Límite: {fecha_limite}\n")
            f.write(f"Estado: {estado}\n")
            f.write("---------------------\n")

    def update_activity_description(self, id_actividad, descripcion):
        """Actualiza la descripción de la actividad en la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="undac",
                database="mineria_db"
            )
            cursor = conexion.cursor()
            update_query = "UPDATE actividades SET descripcion = %s WHERE id = %s;"
            cursor.execute(update_query, (descripcion, id_actividad))
            conexion.commit()
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al actualizar la actividad: {err}")


# Este archivo sería ejecutado como un script independiente o importado en otro archivo.
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    app = GenerarReporte(root)
    app.mainloop()
