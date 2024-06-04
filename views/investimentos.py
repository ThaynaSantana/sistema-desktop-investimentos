import tkinter as tk
from tkinter import font, messagebox
import mysql.connector

def show_investments_screen(username):
    def go_back():
        root.destroy()

    def get_investments(username):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor(dictionary=True)

            # Obter o ID do usuário
            query_user_id = "SELECT id FROM usuarios WHERE username=%s"
            cursor.execute(query_user_id, (username,))
            user_id = cursor.fetchone()['id']

            # Obter os investimentos do usuário
            query_investments = "SELECT tipo, valor_investido, rendimento FROM investimentos WHERE usuario_id=%s"
            cursor.execute(query_investments, (user_id,))
            investments = cursor.fetchall()

            cursor.close()
            conn.close()

            return investments

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
            return []

    # Obter os investimentos do usuário
    user_investments = get_investments(username)

    # Criar nova janela para a tela de investimentos
    root = tk.Tk()
    root.title("Tela de Investimentos")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    bold_font = font.Font(size=16, weight="bold")

    label_title = tk.Label(frame, text="Seus Investimentos", font=bold_font)
    label_title.grid(row=0, column=0, columnspan=3, pady=(10, 10))

    headers = ["Tipo de Investimento", "Valor Investido", "Rendimento"]
    for idx, header in enumerate(headers):
        label = tk.Label(frame, text=header, font=bold_font)
        label.grid(row=1, column=idx, padx=10, pady=5)

    if user_investments:
        for row, investment in enumerate(user_investments):
            label_type = tk.Label(frame, text=investment["tipo"])
            label_type.grid(row=row + 2, column=0, padx=10, pady=5)

            label_value = tk.Label(frame, text=f"R${investment['valor_investido']:.2f}")
            label_value.grid(row=row + 2, column=1, padx=10, pady=5)

            label_return = tk.Label(frame, text=f"{investment['rendimento']*100}%")
            label_return.grid(row=row + 2, column=2, padx=10, pady=5)
    else:
        no_investments_label = tk.Label(frame, text="Nenhum investimento encontrado")
        no_investments_label.grid(row=2, column=0, columnspan=3, pady=5)

    button_back = tk.Button(frame, text="Voltar", command=go_back)
    button_back.grid(row=0, column=2, columnspan=3, pady=(20, 10))

    root.mainloop()

if __name__ == "__main__":
    show_investments_screen()
