import tkinter as tk
from tkinter import Frame
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def obtener_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="undac",
            database="mineria_db"
        )
        cursor = conexion.cursor()
        query = "SELECT estado, COUNT(*) FROM actividades GROUP BY estado"
        cursor.execute(query)
        resultados = cursor.fetchall()
        estados = []
        conteos = []
        for estado, conteo in resultados:
            estados.append(estado)
            conteos.append(conteo)
        cursor.close()
        conexion.close()
        return estados, conteos
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return [], []

def dibujar_grafico(estados, conteos):
    fig, ax = plt.subplots()
    ax.bar(estados, conteos, color=['blue', 'orange'])
    ax.set_xlabel('Estado de la Actividad')
    ax.set_ylabel('Cantidad')
    ax.set_title('Actividades Cumplidas y Pendientes')
    return fig

def mostrar_grafico():
    ventana = tk.Toplevel()  # Crear una nueva ventana
    ventana.title("Visualización de Actividades")

    frame_grafico = Frame(ventana)
    frame_grafico.pack(fill=tk.BOTH, expand=True)

    def actualizar_grafico():
        estados, conteos = obtener_datos()
        fig = dibujar_grafico(estados, conteos)
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    boton_actualizar = tk.Button(ventana, text="Actualizar Gráfico", command=actualizar_grafico)
    boton_actualizar.pack()

    actualizar_grafico()
