import tkinter as tk
from tkinter import messagebox
import mysql.connector


def show_reset_password_screen():

    def go_back():
        root.destroy()

    def reset_password():
        email = entry_email.get()
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if new_password != confirm_password:
            messagebox.showerror("Erro", "A nova senha e a confirmação da nova senha não coincidem.")
            return

        try:
            # Conectar ao banco de dados
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor()

            # Verificar se o email existe no banco de dados
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", email)
            result = cursor.fetchone()

            if result:
                # Atualizar a senha no banco de dados
                cursor.execute("UPDATE usuarios SET senha=%s WHERE email=%s", (new_password, email))
                conn.commit()
                messagebox.showinfo("Sucesso", "Senha alterada com sucesso.")
            else:
                messagebox.showerror("Erro", "Email não encontrado.")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
        finally:
            cursor.close()

    root = tk.Tk()
    root.title("Redefinição de Senha")

    tk.Label(root, text="Email atual").grid(row=0, column=0, padx=10, pady=10)
    entry_email = tk.Entry(root)
    entry_email.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Nova Senha").grid(row=1, column=0, padx=10, pady=10)
    entry_new_password = tk.Entry(root, show="*")
    entry_new_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Confirmar Nova Senha").grid(row=2, column=0, padx=10, pady=10)
    entry_confirm_password = tk.Entry(root, show="*")
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Redefinir Senha", command=reset_password).grid(row=3, column=0, columnspan=2, pady=20)
    tk.Button(root, text="Voltar", command=go_back).grid(row=3, column=1, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    show_reset_password_screen()
