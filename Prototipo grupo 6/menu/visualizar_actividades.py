import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
        self.estado.set("pendiente")

        tk.Button(self, text="Guardar", command=self.guardar_actividad, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=10)

    def guardar_actividad(self):
        nombre = self.nombre_actividad.get()
        fecha_limite = self.fecha_limite.get_date().strftime("%Y-%m-%d")
        estado = self.estado.get()

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
            cursor.execute(query, (nombre, fecha_limite, estado))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Actividad registrada correctamente")
            self.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

class VentanaActividades(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Lista de Actividades")
        self.geometry("600x400")
        self.config(bg=COLOR_CUERPO_PRINCIPAL)

        self.create_widgets()
        self.cargar_actividades()

    def create_widgets(self):
        tk.Label(self, text="Lista de Actividades", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL).pack(pady=10)

        self.actividades_tree = ttk.Treeview(self, columns=("Nombre", "Fecha Límite", "Estado"), show="headings")
        self.actividades_tree.heading("Nombre", text="Nombre")
        self.actividades_tree.heading("Fecha Límite", text="Fecha Límite")
        self.actividades_tree.heading("Estado", text="Estado")
        self.actividades_tree.pack(fill='both', padx=10, pady=5, expand=True)

        tk.Button(self, text="Exportar a TXT", command=self.exportar_a_txt, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=5)
        tk.Button(self, text="Borrar Actividad", command=self.borrar_actividad, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=5)
        tk.Button(self, text="Cambiar Estado", command=self.cambiar_estado, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=5)

    def cargar_actividades(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="undac",
                database="mineria_db"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, fecha_limite, estado FROM actividades")
            for actividad in cursor.fetchall():
                self.actividades_tree.insert("", tk.END, iid=actividad[0], values=actividad[1:])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

    def exportar_a_txt(self):
        try:
            with open("actividades.txt", "w") as file:
                for item in self.actividades_tree.get_children():
                    values = self.actividades_tree.item(item, "values")
                    file.write(f"Nombre: {values[0]}, Fecha Límite: {values[1]}, Estado: {values[2]}\n")
            messagebox.showinfo("Éxito", "Actividades exportadas a actividades.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a TXT: {e}")

    def borrar_actividad(self):
        seleccionado = self.actividades_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Debe seleccionar una actividad para borrar")
            return

        actividad_id = seleccionado[0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar esta actividad?"):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="undac",
                    database="mineria_db"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM actividades WHERE id = %s", (actividad_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.actividades_tree.delete(actividad_id)
                messagebox.showinfo("Éxito", "Actividad borrada correctamente")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

    def cambiar_estado(self):
        seleccionado = self.actividades_tree.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Debe seleccionar una actividad para cambiar el estado")
            return

        actividad_id = seleccionado[0]
        estado_actual = self.actividades_tree.item(actividad_id, "values")[2]

        estado_ventana = tk.Toplevel(self)
        estado_ventana.title("Seleccionar Nuevo Estado")
        estado_ventana.geometry("300x150")
        estado_ventana.config(bg=COLOR_CUERPO_PRINCIPAL)

        tk.Label(estado_ventana, text="Selecciona el nuevo estado:", bg=COLOR_CUERPO_PRINCIPAL).pack(pady=10)

        estado_combobox = ttk.Combobox(estado_ventana, values=["pendiente", "cumplida"])
        estado_combobox.pack(pady=5)
        estado_combobox.set(estado_actual)

        def actualizar_estado():
            nuevo_estado = estado_combobox.get()
            if nuevo_estado not in ["pendiente", "cumplida"]:
                messagebox.showwarning("Error", "Estado no válido. Debe ser 'pendiente' o 'cumplida'.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="undac",
                    database="mineria_db"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE actividades SET estado = %s WHERE id = %s", (nuevo_estado, actividad_id))
                conn.commit()
                cursor.close()
                conn.close()
                self.actividades_tree.item(actividad_id, values=(self.actividades_tree.item(actividad_id, "values")[0], self.actividades_tree.item(actividad_id, "values")[1], nuevo_estado))
                estado_ventana.destroy()
                messagebox.showinfo("Éxito", "Estado de la actividad actualizado correctamente")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

        tk.Button(estado_ventana, text="Actualizar", command=actualizar_estado, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(pady=10)
