import tkinter as tk
from tkinter import messagebox, font
from DAO import UsuarioDAO
from PIL import Image, ImageTk
import qrcode
from tkinter import ttk
import os
import tempfile
class SistemaColegial:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.iniciar_interfaz()

    def iniciar_interfaz(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema Colegial")
        self.ventana.configure(bg='#f7f7f7')
        self.ventana.geometry("1080x1080")

        titulo_fuente = font.Font(family="Helvetica", size=12, weight="bold")
        texto_fuente = font.Font(family="Helvetica", size=10)

        frame_entrada = tk.Frame(self.ventana, bg='#f7f7f7')
        frame_entrada.pack(padx=10, pady=10, fill='x', expand=True)

        self.tipo_usuario_var = tk.StringVar()
        self.tipo_usuario_var.set("Estudiante") 
        tipos_usuario = ["Estudiante", "Director", "Inspector"]
        tk.OptionMenu(frame_entrada, self.tipo_usuario_var, *tipos_usuario).pack(padx=5, pady=5, fill='x', expand=True)


        tk.Label(frame_entrada, text="Nombre:", bg='#f7f7f7', font=texto_fuente).pack(fill='x', expand=True)
        self.entry_nombre = tk.Entry(frame_entrada, font=texto_fuente)
        self.entry_nombre.pack(padx=5, pady=5, fill='x', expand=True)

        tk.Label(frame_entrada, text="RUT:", bg='#f7f7f7', font=texto_fuente).pack(fill='x', expand=True)
        self.entry_rut = tk.Entry(frame_entrada, font=texto_fuente)
        self.entry_rut.pack(padx=5, pady=5, fill='x', expand=True)

        tk.Label(frame_entrada, text="Contraseña:", bg='#f7f7f7', font=texto_fuente).pack(fill='x', expand=True)
        self.entry_contrasena = tk.Entry(frame_entrada, show="*", font=texto_fuente)
        self.entry_contrasena.pack(padx=5, pady=5, fill='x', expand=True)

        frame_botones = tk.Frame(self.ventana, bg='#f7f7f7')
        frame_botones.pack(padx=10, pady=10, fill='x', expand=True)

        boton_registro = tk.Button(frame_botones, text="Registrar", command=self.registrar, font=texto_fuente, bg="#4f5d76", fg="white")
        boton_registro.pack(padx=5, pady=5, fill='x', expand=True)

        boton_inicio_sesion = tk.Button(frame_botones, text="Iniciar Sesión", command=self.iniciar_sesion, font=texto_fuente, bg="#4f5d76", fg="white")
        boton_inicio_sesion.pack(padx=5, pady=5, fill='x', expand=True)

        self.ventana.mainloop()

    def registrar(self):
        nombre = self.entry_nombre.get()
        rut = self.entry_rut.get()
        contrasena = self.entry_contrasena.get()
        tipo_usuario = self.tipo_usuario_var.get()
        try:
            self.usuario_dao.registrar_usuario(nombre, rut, contrasena, tipo_usuario)
            messagebox.showinfo("Registro exitoso", f"{tipo_usuario} registrado exitosamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def iniciar_sesion(self):
        rut = self.entry_rut.get()
        contrasena = self.entry_contrasena.get()

        if self.usuario_dao.validar_usuario(rut, contrasena):
            tipo_usuario = self.usuario_dao.usuarios[rut]['tipo_usuario']
            nombre = self.usuario_dao.usuarios[rut]['nombre']

            if tipo_usuario == "Estudiante":
                self.mostrar_ventana_estudiante(nombre)
            elif tipo_usuario == "Director":
                self.mostrar_ventana_director(nombre)
            elif tipo_usuario == "Inspector":
                self.mostrar_ventana_inspector()
            else:
                messagebox.showinfo("Inicio de sesión", f"{tipo_usuario} {nombre} ha iniciado sesión.")

    def mostrar_ventana_director(self, nombre):
        ventana_director = tk.Toplevel(self.ventana)
        ventana_director.title("Director - Lista de Estudiantes")
        ventana_director.geometry("600x400")
        frame_lista = tk.Frame(ventana_director)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        columns = ("Nombre", "RUT", "QR")
        tree = ttk.Treeview(frame_lista, columns=columns, show="headings")
        tree.column("QR", width=200)
        tree.heading("Nombre", text="Nombre")
        tree.heading("RUT", text="RUT")
        tree.heading("QR", text="Código QR")

        for estudiante in self.usuario_dao.obtener_estudiantes():
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(estudiante['nombre'])
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")

            temp_file = tempfile.NamedTemporaryFile(delete=False)
            img_qr.save(temp_file.name + ".png")

            tree.insert("", tk.END, values=(estudiante['nombre'], estudiante['rut'], temp_file.name + ".png"))

        tree.pack(fill=tk.BOTH, expand=True)

        def on_item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                qr_image_path = item['values'][2]
                update_qr_image(qr_image_path)

        tree.bind("<<TreeviewSelect>>", on_item_selected)

        frame_qr = tk.Frame(ventana_director)
        frame_qr.pack(fill=tk.BOTH, expand=True)

        qr_label = tk.Label(frame_qr)
        qr_label.pack()

        def update_qr_image(path):
            img = Image.open(path)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(img)
            qr_label.config(image=qr_photo)
            qr_label.image = qr_photo

    def mostrar_ventana_inspector(self):
        ventana_inspector = tk.Toplevel(self.ventana)
        ventana_inspector.title("Inspector - Lista de Usuarios")
        ventana_inspector.geometry("500x400")

        columnas = ("Nombre", "RUT", "Tipo")
        tree = tk.ttk.Treeview(ventana_inspector, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(expand=True, fill='both', side='left')

        scrollbar = tk.Scrollbar(ventana_inspector, orient='vertical', command=tree.yview)
        scrollbar.pack(fill='y', side='right')
        tree.configure(yscrollcommand=scrollbar.set)

        for rut, usuario in self.usuario_dao.usuarios.items():
            if usuario['tipo_usuario'] in ['Estudiante', 'Director']:
                tree.insert("", tk.END, values=(usuario['nombre'], rut, usuario['tipo_usuario']))

    def mostrar_ventana_estudiante(self, nombre):
        ventana_estudiante = tk.Toplevel(self.ventana)
        ventana_estudiante.title("Perfil del Estudiante")
        ventana_estudiante.configure(bg='#f7f7f7')
        ventana_estudiante.geometry("300x300")

        texto_fuente = font.Font(family="Helvetica", size=10)

        tk.Label(ventana_estudiante, text=f"Bienvenido, {nombre}", bg='#f7f7f7', font=texto_fuente).pack(pady=10)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(nombre)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")

        img_qr = img_qr.convert("RGB")
        img_temp = Image.new("RGB", img_qr.size)
        img_temp.paste(img_qr)
        img_tk = ImageTk.PhotoImage(image=img_temp)

        label_imagen = tk.Label(ventana_estudiante, image=img_tk)
        label_imagen.image = img_tk 
        label_imagen.pack(pady=10)
    def generar_qr(self, nombre):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(nombre)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.show()

if __name__ == "__main__":
    app = SistemaColegial()