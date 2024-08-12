import tkinter as tk
from tkinter import messagebox
import hashlib
from PIL import Image, ImageTk
from formularios.form_maestro_design import FormularioMaestroDesign

# Diccionario de usuarios y contraseñas hash
users = {"usuario": hashlib.sha256("undac".encode()).hexdigest()}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Login")
        self.geometry("1024x600")
        self.configure(bg='#000')

        # Fondo de la ventana
        self.background_image = Image.open("./imagenes/fondo6.png")
        self.background_image = self.background_image.resize((1024, 600), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.bg_label = tk.Label(self, image=self.background_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menú en la esquina superior izquierda
        self.menu_frame = tk.Frame(self, bg='#000')
        self.menu_frame.place(relx=0.25, rely=0.1, anchor=tk.CENTER)
        for text in ["Inicio", "Nosotros", "Beneficios", "A cerca de"]:
            btn = tk.Button(self.menu_frame, text=text, bg='#000', fg='white', font=("Segoe UI", 12, "bold"), relief='flat')
            btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Barra de búsqueda sobre el bloque de inicio de sesión
        self.search_frame = tk.Frame(self, bg='#000')
        self.search_frame.place(relx=0.75, rely=0.1, anchor=tk.CENTER)  # Ubicación del marco de búsqueda
        
        search_label = tk.Label(self.search_frame, text="Buscar:", bg='#000', fg='#fff', font=("Segoe UI", 12, "bold"))
        search_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Segoe UI", 12), bg='#333', fg='#fff', insertbackground='white')
        self.search_entry.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.X, expand=True)

        search_button = tk.Button(self.search_frame, text="Buscar", bg='#000', fg='white', font=("Segoe UI", 12, "bold"), relief='flat')
        search_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Marco para los textos y la imagen a la izquierda
        self.left_frame = tk.Frame(self, bg='#000', width=300)
        self.left_frame.place(relx=0.18, rely=0.55, anchor=tk.CENTER)  # Desplazar hacia el centro

        # Texto de bienvenida
        tk.Label(self.left_frame, text="Compañía minera\nUNDAC\n\n", font=("Segoe UI", 20, "bold"), fg='#fff', bg='#000').pack(pady=10)
        tk.Label(self.left_frame, text="¡Bienvenido!\nEstamos encantados de\ntenerte de nuevo.", font=("Segoe UI", 18), fg='#fff', bg='#000').pack(pady=10)
        tk.Label(self.left_frame, text="Gracias a ti, estamos creciendo\nmás allá de nuestras expectativas.\nCompartamos el éxito cada día.", font=("Segoe UI", 12), fg='#fff', bg='#000', wraplength=300).pack(pady=10)

        # Imagen de redes sociales
        self.social_image = Image.open("./imagenes/sociales.png")
        self.social_image = self.social_image.resize((100, 50), Image.LANCZOS)
        self.social_photo = ImageTk.PhotoImage(self.social_image)
        self.social_label = tk.Label(self.left_frame, image=self.social_photo, bg='#000')
        self.social_label.pack(pady=10)

        # Marco para el formulario de inicio de sesión a la derecha
        self.form_frame = tk.Frame(self, bg='#000')
        self.form_frame.place(relx=0.82, rely=0.5, anchor=tk.CENTER)  # Desplazar hacia el centro

        # Encabezado
        tk.Label(self.form_frame, text="Iniciar Sesión", font=("Segoe UI", 20, "bold"), fg='#fff', bg='#000').pack(pady=20)

        # Entrada de usuario
        tk.Label(self.form_frame, text="Nombre de usuario:", bg='#000', fg='#fff', font=("Segoe UI", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.form_frame, font=("Segoe UI", 12), bg='#333', fg='#fff', insertbackground='white')
        self.username_entry.pack(pady=5, padx=20, fill=tk.X)

        # Entrada de contraseña
        tk.Label(self.form_frame, text="Contraseña:", bg='#000', fg='#fff', font=("Segoe UI", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=("Segoe UI", 12), bg='#333', fg='#fff', insertbackground='white')
        self.password_entry.pack(pady=5, padx=20, fill=tk.X)

        # Botones de iniciar sesión y registrarse
        login_button = tk.Button(self.form_frame, text="Iniciar sesión", command=self.login, bg='#0d9ea3', fg='white', font=("Segoe UI", 12), relief='flat')
        login_button.pack(pady=10, padx=10, fill=tk.X)  # Añadir margen
        register_button = tk.Button(self.form_frame, text="Registrarse", command=self.register, bg='#5cb85c', fg='white', font=("Segoe UI", 12), relief='flat')
        register_button.pack(pady=10, padx=10, fill=tk.X)  # Añadir margen

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in users and users[username] == hash_password(password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    def register(self):
        # Lógica de registro (puedes reutilizar el código de registro anterior)
        pass

    def open_main_window(self):
        self.destroy()  # Cierra la ventana de login
        main_window = FormularioMaestroDesign()  # Abre la ventana principal
        main_window.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
