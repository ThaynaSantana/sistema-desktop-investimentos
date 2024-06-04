import tkinter as tk
from tkinter import messagebox
import mysql.connector

def show_withdraw_screen(username):
    # Criar nova janela para a tela de saque
    root = tk.Tk()
    root.title("Tela de Saque")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    def clear_frame():
        for widget in frame.winfo_children():
            widget.grid_remove()

    def go_back():
        root.destroy()
        from views.home import show_home_screen
        show_home_screen(username)

    def withdraw():
        amount = entry_amount.get()

        if not amount:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o valor a ser sacado.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Valor Inválido", "Por favor, insira um valor numérico.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor()

            # Obter o ID do usuário
            query_user_id = "SELECT id, saldo FROM usuarios WHERE username=%s"
            cursor.execute(query_user_id, (username,))
            user_data = cursor.fetchone()

            if user_data is None:
                messagebox.showerror("Erro", "Usuário não encontrado.")
                conn.close()
                return

            user_id, saldo = user_data

            if amount > saldo:
                messagebox.showwarning("Saldo Insuficiente", "Você não tem saldo suficiente para esse saque.")
                conn.close()
                return

            # Atualizar saldo do usuário no banco de dados
            query_update_saldo = "UPDATE usuarios SET saldo = saldo - %s WHERE id = %s"
            cursor.execute(query_update_saldo, (amount, user_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Saque Realizado", f"Você sacou R${amount:.2f}.")
            go_back()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

    label_amount = tk.Label(frame, text="Valor a ser Sacado:")
    label_amount.grid(row=0, column=0, pady=5, sticky="e")

    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=0, column=1, pady=5, sticky="w")

    button_withdraw = tk.Button(frame, text="Sacar", command=withdraw)
    button_withdraw.grid(row=1, column=0, pady=10)

    button_cancel = tk.Button(frame, text="Cancelar", command=go_back)
    button_cancel.grid(row=1, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_withdraw_screen()
