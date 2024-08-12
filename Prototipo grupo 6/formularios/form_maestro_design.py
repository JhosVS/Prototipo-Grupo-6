# form_maestro_design.py
import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA

import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from menu.visualizar_actividades import VentanaActividades
import menu.registro_actividades as registro_actividades
import menu.barra as barra
import menu.sistema_pagos as sistema_pagos
import menu.historial_pagos as historial_pagos
import menu.generar_reporte as generar_reporte

class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png", (560, 136))
        self.perfil = util_img.leer_imagen("./imagenes/Perfil.png", (100, 100))
        self.font_awesome = font.Font(family='FontAwesome', size=12)
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.title('Ingenieria de Software II')
        self.iconbitmap("./imagenes/logo.ico")
        util_ventana.centrar_ventana(self, 1024, 600)

    def setup_ui(self):
        self.create_panels()
        self.create_top_bar()
        self.create_side_menu()
        self.create_main_body()

    def create_panels(self):
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='y')

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def create_top_bar(self):
        tk.Label(self.barra_superior, text="PROTOTIPO", fg="#fff", font=("Roboto", 15),
                 bg=COLOR_BARRA_SUPERIOR, pady=10, width=16).pack(side=tk.LEFT)

        tk.Button(self.barra_superior, text="\uf0c9", font=self.font_awesome, command=self.toggle_panel,
                  bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white").pack(side=tk.LEFT)

        tk.Label(self.barra_superior, text="UnEjemplo@undac.edu.pe", fg="#fff",
                 font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20).pack(side=tk.RIGHT)

    def create_side_menu(self):
        tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL).pack(side=tk.TOP, pady=10)

        buttons_info = [
            ("Mostrar Actividades", "\uf109", self.open_activities),
            ("Agregar Actividades", "\uf067", self.open_add_activities),
            ("Generar Reporte", "\uf0f6", lambda: generar_reporte.GenerarReporte(self)),
            ("Abrir Barra", "\uf085", self.open_bar),
            ("Sistema de Pagos", "\uf03e", self.open_payment_system),
            ("Historial de Pagos", "\uf19c", self.open_payment_history),
        ]

        for text, icon, command in buttons_info:
            button = tk.Button(self.menu_lateral, text=f"  {icon}    {text}", anchor="w", font=self.font_awesome,
                               bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, command=command)
            button.pack(side=tk.TOP)
            self.bind_hover_events(button)

    def create_main_body(self):
        tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL).place(x=0, y=0, relwidth=1, relheight=1)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white'))
        button.bind("<Leave>", lambda event: button.config(bg=COLOR_MENU_LATERAL, fg='white'))

    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def open_activities(self):
        VentanaActividades(self)

    def open_add_activities(self):
        registro_actividades.VentanaRegistroActividades(self)

    def open_bar(self):
        barra.mostrar_grafico()

    def open_payment_system(self):
        # Crear instancias necesarias
        db_connector = sistema_pagos.MySQLConnector()
        employee_repo = sistema_pagos.EmployeeRepository(db_connector)
        payment_repo = sistema_pagos.PaymentRepository(db_connector)
        report_gen = sistema_pagos.ReportGenerator()

        # Instanciar SistemaPagos con todos los argumentos requeridos
        sistema_pagos.SistemaPagos(
            self,
            db_connector,
            employee_repo,
            payment_repo,
            report_gen
        )

    def open_payment_history(self):
        historial_pagos.HistorialPagos(self)

    def open_payment_report(self):
        generar_reporte.GenerarReporte(self)

if __name__ == "__main__":
    app = FormularioMaestroDesign()
    app.mainloop()
