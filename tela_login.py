import tkinter as tk
from tkinter import messagebox
import mysql.connector
from controllers.esqueci_minha_senha import show_reset_password_screen
from views.home import show_home_screen
from controllers.tela_registro import show_register_screen

def show_login_screen():
    # Função para o link ESQUECI MINHA SENHA
    def forgot_password():
        show_reset_password_screen()

    # Função para o botão REGISTRO
    def register():
        show_register_screen()

    # Função para o botão ENTRAR
    def login():
        username = entry_username.get()
        password = entry_password.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor()

            #Verificação se existe essa conta de usuario
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username,password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Logado Sucesso!", "Login feito com sucesso!")
                root.destroy()
                show_home_screen(username)
            else:
                messagebox.showerror("Erro","Não foi possivel fazer login da conta inserida.")
        finally:
            cursor.close()

    # Configuração da janela principal
    root = tk.Tk()
    root.title("[Baú] - Tela de Login")
    root.geometry("400x300")  # Largura x Altura

    # Frame para o formulário de login
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    # Configurar a grade do frame para centralizar os elementos
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_rowconfigure(3, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Label de titulo
    label_title = tk.Label(frame, text="Tela de Login do BAÚ", font=("Helvetica", 24))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Rotulo e input USUARIO
    label_username = tk.Label(frame, text="Usuário:")
    label_username.grid(row=1, column=0, pady=5, sticky="e")
    entry_username = tk.Entry(frame)
    entry_username.grid(row=1, column=1, pady=5)

    # Rotulo e input SENHA
    label_password = tk.Label(frame, text="Senha:")
    label_password.grid(row=2, column=0, pady=5, sticky="e")
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=2, column=1, pady=5)

    # Hyperlink "esqueci minha senha"
    link_forgot_password = tk.Label(frame, text="Esqueci minha senha", fg="blue", cursor="hand2")
    link_forgot_password.grid(row=3, column=1, pady=5, sticky="w")
    link_forgot_password.bind("<Button-1>", lambda e: forgot_password())

    # Botão "registre-se"
    button_register = tk.Button(frame, text="Registre-se", command=register)
    button_register.grid(row=4, column=0, pady=10)

    # Botão "entrar"
    button_login = tk.Button(frame, text="Entrar", command=login)
    button_login.grid(row=4, column=1, pady=10)

    # Loop principal da aplicação
    root.mainloop()

if __name__ == "__main__":
    show_login_screen()

