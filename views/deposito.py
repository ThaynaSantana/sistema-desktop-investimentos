import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
from barcode import Code39
from barcode.writer import ImageWriter
import random
import os
import mysql.connector


def show_deposit_screen(username):
    def on_closing():
        if os.path.exists("pix_qrcode.png"):
            os.remove("pix_qrcode.png")
        if os.path.exists("boleto_barcode.png"):
            os.remove("boleto_barcode.png")
        root.destroy()

    def go_back():
        root.destroy()
        from views.home import show_home_screen
        show_home_screen(username)

    def generate_pix_qr_code(amount):
        # Gerar código QR para o PIX
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        pix_content = f"Valor={amount}"
        qr.add_data(pix_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Salvar imagem temporariamente
        img.save("pix_qrcode.png")

        # Carregar e exibir a imagem na janela Tkinter
        pix_img = Image.open("pix_qrcode.png")
        pix_img = pix_img.resize((250, 250))
        pix_photo = ImageTk.PhotoImage(pix_img)

        label_image.config(image=pix_photo)
        label_image.image = pix_photo  # Manter referência à imagem

    def generate_boleto_barcode(amount):
        #Gerar código de barras para o boleto
        boleto_code = random.randint(100000000000, 999999999999)  # Exemplo de código aleatório de 12 dígitos
        code = Code39(str(boleto_code), writer=ImageWriter())
        code.save("boleto_barcode")

        #Carregar e exibir a imagem na janela Tkinter
        boleto_img = Image.open("boleto_barcode.png")
        boleto_img = boleto_img.resize((350, 100))
        boleto_photo = ImageTk.PhotoImage(boleto_img)

        label_image.config(image=boleto_photo)
        label_image.image = boleto_photo

    def deposit():
        amount = entry_amount.get()
        payment_method = payment_var.get()

        if not amount:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o valor a ser depositado.")
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

            query_user_id = "SELECT id FROM usuarios WHERE username=%s"
            cursor.execute(query_user_id, (username,))
            user_id = cursor.fetchone()[0]

            #Atualiza saldo
            query_update_saldo = "UPDATE usuarios SET saldo = saldo + %s WHERE id = %s"
            cursor.execute(query_update_saldo, (amount, user_id))
            conn.commit()
            conn.close()

            if payment_method == "PIX QR Code":
                generate_pix_qr_code(amount)

            elif payment_method == "Boleto":
                generate_boleto_barcode(amount)
            else:
                messagebox.showwarning("Método de Pagamento Inválido", "Por favor, selecione um método de pagamento.")

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

    root = tk.Tk()
    root.title("[Bau] - Depósito de Dinheiro")

    #Frame
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    #Label e entrada para o valor
    label_amount = tk.Label(frame, text="Valor a ser depositado:")
    label_amount.grid(row=0, column=0, pady=5, sticky="e")
    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=0, column=1, pady=5)

    # Radio buttons para escolher o método de pagamento
    payment_var = tk.StringVar()
    label_payment = tk.Label(frame, text="Método de Pagamento:")
    label_payment.grid(row=1, column=0, pady=5, sticky="e")

    radio_pix = tk.Radiobutton(frame, text="PIX QR Code", variable=payment_var, value="PIX QR Code")
    radio_pix.grid(row=1, column=1, pady=5, sticky="w")

    radio_boleto = tk.Radiobutton(frame, text="Boleto", variable=payment_var, value="Boleto")
    radio_boleto.grid(row=2, column=1, pady=5, sticky="w")

    # Botão para depositar
    button_deposit = tk.Button(frame, text="Depositar", command=deposit)
    button_deposit.grid(row=3, column=0, columnspan=2, pady=10)

    # Label para exibir a imagem
    label_image = tk.Label(frame)
    label_image.grid(row=4, column=0, columnspan=2, pady=10)

    # Botão de voltar
    button_come_back = tk.Button(frame, text="Voltar", command=go_back)
    button_come_back.grid(row=3, column=1, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    show_deposit_screen()
