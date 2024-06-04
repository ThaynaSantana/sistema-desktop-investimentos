import tkinter as tk
from tkinter import messagebox
import mysql.connector

def show_invest_screen(username):
    def go_back():
        root.destroy()
        from views.home import show_home_screen
        show_home_screen(username)

    def invest():
        investment_type = investment_var.get()
        amount = entry_amount.get()

        if not amount:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o valor a ser investido.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Valor Inválido", "Por favor, insira um valor numérico.")
            return

        # Rendimentos
        rendimentos = {
            "CDB": 1.02,
            "LCA": 0.738, # 90% do CDI, CDB=0.82%
            "LCI": 0.738, # 90% do CDI, CDB=0.82%
            "Tesouro Direto": 0.87 # 87% do CDB
        }

        # Obter o rendimento baseado no tipo de investimento
        rendimento = rendimentos.get(investment_type)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor()

            # Obter o ID do usuário
            query_user_id = "SELECT id FROM usuarios WHERE username=%s"
            cursor.execute(query_user_id, (username,))
            user_id = cursor.fetchone()[0]

            # Verificar saldo suficiente
            query_saldo = "SELECT saldo FROM usuarios WHERE id=%s"
            cursor.execute(query_saldo, (user_id,))
            saldo = cursor.fetchone()[0]

            if amount > saldo:
                messagebox.showwarning("Saldo Insuficiente", "Você não tem saldo suficiente para esse investimento.")
                conn.close()
                return

            # Atualizar saldo na tabela usuarios
            query_update_saldo = "UPDATE usuarios SET saldo = saldo - %s WHERE id = %s"
            cursor.execute(query_update_saldo, (amount, user_id))

            # Inserir investimento na tabela investimentos
            query_insert_investment = "INSERT INTO investimentos (usuario_id, tipo, valor_investido, rendimento) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_insert_investment, (user_id, investment_type, amount, rendimento))

            conn.commit()
            messagebox.showinfo("Investimento Realizado", f"Você investiu R${amount:.2f} em {investment_type}.")
            go_back()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

        finally:
            conn.close()

    root = tk.Tk()
    root.title("Tela de Investimento")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    label_type = tk.Label(frame, text="Tipo de Investimento:")
    label_type.grid(row=0, column=0, pady=5, sticky="e")

    investment_var = tk.StringVar(value="CDB")
    option_menu = tk.OptionMenu(frame, investment_var, "CDB", "LCA", "LCI", "Tesouro Direto")
    option_menu.grid(row=0, column=1, pady=5, sticky="w")

    label_amount = tk.Label(frame, text="Valor a ser Investido:")
    label_amount.grid(row=1, column=0, pady=5, sticky="e")

    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=1, column=1, pady=5, sticky="w")

    button_invest = tk.Button(frame, text="Investir", command=invest)
    button_invest.grid(row=2, column=0, pady=10)

    button_cancel = tk.Button(frame, text="Cancelar", command=go_back)
    button_cancel.grid(row=2, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_invest_screen()
