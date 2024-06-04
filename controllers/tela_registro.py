import tkinter as tk
from tkinter import messagebox
import mysql.connector

def show_register_screen():
    def register_user():
        name = entry_name.get()
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()
        tel = entry_tel.get()

        if not name or not username or not password or not email:
            messagebox.showwarning("Entrada inválida", "Todos os campos são obrigatórios")
            return

        try:
            # Conectando ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = db.cursor()

            # Inserindo os dados do usuário no banco de dados
            query = "INSERT INTO usuarios (name, username, password, email, tel, saldo) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, username, password, email, tel, 0))
            db.commit()
            root.destroy()
            messagebox.showinfo("Registro bem-sucedido", "Usuário registrado com sucesso!")


        except mysql.connector.Error as err:
            messagebox.showerror("Erro de banco de dados", f"Erro ao registrar usuário: {err}")
        finally:
            cursor.close()
            db.close()

    # Configuração da janela principal
    root = tk.Tk()
    root.title("[Baú] - Tela de Registro")

    # Ajustar o tamanho da janela
    root.geometry("400x300")  # Largura x Altura

    # Frame para o formulário de registro
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    # Label de título grande
    label_title = tk.Label(frame, text="Registro", font=("Helvetica", 24))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Rotulo e input NOME
    label_name = tk.Label(frame, text="Nome:")
    label_name.grid(row=1, column=0, pady=5, sticky="e")
    entry_name = tk.Entry(frame)
    entry_name.grid(row=1, column=1, pady=5)

    # Rotulo e inpute USUARIO
    label_username = tk.Label(frame, text="Nome de Usuário:")
    label_username.grid(row=2, column=0, pady=5, sticky="e")
    entry_username = tk.Entry(frame)
    entry_username.grid(row=2, column=1, pady=5)

    # Rotulo e input SENHA
    label_password = tk.Label(frame, text="Senha:")
    label_password.grid(row=3, column=0, pady=5, sticky="e")
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=3, column=1, pady=5)

    # Rotulo e input EMAIL
    label_email = tk.Label(frame, text="Email:")
    label_email.grid(row=4, column=0, pady=5, sticky="e")
    entry_email = tk.Entry(frame)
    entry_email.grid(row=4, column=1, pady=5)

    # Rotulo e input TELEFONE
    label_tel = tk.Label(frame, text="Telefone:")
    label_tel.grid(row=5, column=0, pady=5, sticky="e")
    entry_tel = tk.Entry(frame)
    entry_tel.grid(row=5, column=1, pady=5)

    # Botão "Registrar"
    button_register = tk.Button(frame, text="Registrar", command=register_user)
    button_register.grid(row=6, column=0, columnspan=2, pady=10)

    # Loop principal da aplicação
    root.mainloop()

if __name__ == "__main__":
    show_register_screen()

