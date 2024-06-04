import tkinter as tk
from tkinter import font, messagebox
import mysql.connector

def show_home_screen(username):

    def describe_cdb():
        messagebox.showinfo("Explicação do CDB","""#O que é CDB?
Se você já investiu no Tesouro Direto, sabe que quem compra títulos públicos na prática “empresta” dinheiro para o governo fazer a máquina pública girar. Da mesma forma, quem investe em debêntures empresta recursos para uma empresa realizar grandes projetos. A lógica é exatamente a mesma nos certificados de depósito bancário: quem compra CDBs empresta dinheiro para os bancos financiarem suas atividades de crédito.

Os bancos captam dinheiro com os CDBs oferecendo em troca uma remuneração – os juros – aos investidores, por um determinado período. Os recursos são usados por essas instituições para conceder empréstimos a outras pessoas.

Só ficam de fora os valores que os bancos são obrigados a recolher como depósito compulsório junto ao Banco Central – cerca de um terço do que captam. Esse volume de recursos não pode ser emprestado. A obrigação serve exatamente para que o governo consiga controlar o dinheiro em circulação na economia.

Como funciona
O investimento em CDBs se parece bastante com outros produtos de renda fixa. Entenda aqui os detalhes desse tipo de aplicação:

Rentabilidade
Quanto rende um CDB? A resposta é: depende. Existem vários tipos de CDBs, e cada um possui uma característica bem particular. Os três modelos mais comuns são: Saiba Mais em InfoMoney -> https://www.infomoney.com.br/guias/cdb/""")

    def describe_lca():
        messagebox.showinfo("Explicação do LCA","""O que é LCA?
A Letra de Crédito do Agronegócio (LCA) é um título de renda fixa emitido por instituições financeiras públicas e privadas. 

Seus princípios são muito semelhantes à Letra de Crédito Imobiliário (LCI). A principal diferença está na destinação dos valores captados. Explicaremos um pouco mais abaixo! 

O valor captado na LCA é destinado, principalmente, para os empréstimos a produtores rurais que precisam do dinheiro para comprar maquinário e insumos. Assim, ao mesmo tempo em que pode colher bons rendimentos, o investidor ajuda indiretamente a impulsionar um setor vital para o país. Saiba mais em: https://conteudos.xpi.com.br/aprenda-a-investir/relatorios/o-que-e-lca/""")
    def describe_lci():
        messagebox.showinfo("Explicação do LCI",""" Na LCI a emissão do papel é usada para financiar as atividades do segmento imobiliário. Já na LCA, o foco são as operações do agronegócio. As duas emissões possuem características semelhantes, mas no LCA não existe a cobrança de imposto sobre operações financeiras (IOF) para resgates em menos de 30 dias. 
O que é LCI?
LCI significa Letra de Crédito Imobiliário.

São títulos de Renda Fixa emitidos por instituições financeiras com o objetivo de financiar o setor imobiliário.

Características da LCI:

- Possui garantia do "Fundo Garantidor de Créditos - FGC", limitado a R$250 mil (por CPF e por instituição emissora);
- Não há a incidência de Imposto de Renda;
- Na NuInvest, a taxa de administração é ZERO.
Saiba mais em: Ajuda.NuInvest -> https://ajuda.nuinvest.com.br/hc/pt-br/articles/227053607-O-que-%C3%A9-LCI""")

    def describe_tesouro_direto():
        messagebox.showinfo("Explicação do Tesouro Direto", """O que é o Tesouro Direto?
Criado em 2002, o Tesouro Direto foi desenvolvido pelo governo federal para captar recursos e financiar as dívidas públicas.
                                    
Sob gestão do Tesouro Nacional, ele se assemelha a uma operação de crédito pessoal, em que uma pessoa física ou jurídica empresta dinheiro ao governo em troca de um rendimento futuro.
                                    
Nos últimos anos, esse tipo de investimento tem crescido entre a população, especialmente pela facilidade em se aplicar e pelo baixo risco de crédito.
                                    
Na operação, o investidor compra um título público por um preço e, tempos depois, recebe aquela mesma importância acrescida de juros.
                                    
Ao emitir um título de crédito, o Tesouro Direto define o valor de cada unidade, a remuneração a ser paga por ela e a data de vencimento.
                                    
Atualmente, há opções a partir de R$ 30, que contam com valorização anual de 11% e pagamento para 2024.
Saiba Mais em: CNN Brasil -> https://www.cnnbrasil.com.br/economia/tesouro-direto/""")

    def go_deposit():
        root.destroy()
        from views.deposito import show_deposit_screen
        show_deposit_screen(username)

    def go_invest():
        root.destroy()
        from views.investir import show_invest_screen
        show_invest_screen(username)

    def go_withdraw():
        root.destroy()
        from views.saque import show_withdraw_screen
        show_withdraw_screen(username)

    def go_investments():
        from views.investimentos import show_investments_screen
        show_investments_screen(username)

    def get_data(username):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_bau"
            )
            cursor = conn.cursor(dictionary=True)

            # Obter dados do usuário
            query = "SELECT * FROM usuarios WHERE username=%s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                # Obter dados de investimentos
                user_id = user_data['id']
                query_invest = "SELECT * FROM investimentos WHERE usuario_id=%s"
                cursor.execute(query_invest, (user_id,))
                investments = cursor.fetchall()

                # Calcular totais de investimentos e rendimentos
                total_investido = sum(inv['valor_investido'] for inv in investments) if investments else 0
                rendimento_total = sum(inv['rendimento'] for inv in investments) if investments else 0

                user_data['total_investido'] = total_investido
                user_data['rendimento_total'] = rendimento_total
            else:
                user_data = {
                    'name': 'Desconhecido',
                    'saldo': 0,
                    'total_investido': 0,
                    'rendimento_total': 0
                }

            cursor.close()
            conn.close()
            return user_data

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
            return None

    # Obter os dados do usuário
    user = get_data(username)

    if not user:
        tk.messagebox.showerror("Erro", "Não foi possível obter os dados do usuário.")
        return

    root = tk.Tk()
    root.title("Tela Inicial")

    # Definir uma fonte grande e em negrito
    bold_font = font.Font(size=16, weight="bold")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    # Linha 1: Bem-vindo e Rendendo 102% CDI
    label_welcome = tk.Label(frame, text=f"Bem-vindo, {user['name']}", font=bold_font)
    label_welcome.grid(row=0, column=0, sticky="w")

    label_cdi = tk.Label(frame, text="Rendendo 102% CDI")
    label_cdi.grid(row=0, column=2, sticky="w")

    # Linha 2: Saldo
    label_saldo = tk.Label(frame, text=f"Saldo R${user['saldo']:.2f}")
    label_saldo.grid(row=1, column=0, columnspan=2, sticky="w")

    # Linha 3: Total investido
    label_total_investido = tk.Label(frame, text=f"Total investido R${user['total_investido']:.2f}")
    label_total_investido.grid(row=2, column=0, columnspan=2, sticky="w")

    # Linha 4: Rendimentos Totais
    label_rendimento_total = tk.Label(frame, text=f"Rendimentos Totais: +{user['rendimento_total']*100}%")
    label_rendimento_total.grid(row=3, column=0, columnspan=2, sticky="w")

    # Linha 5: Título "Ativos"
    label_ativos = tk.Label(frame, text="Ativos", font=bold_font)
    label_ativos.grid(row=4, column=0, pady=(10, 5), sticky="w")

    # Linha 6: Hyperlinks para ativos
    link_cdb = tk.Label(frame, text="CDB", fg="blue", cursor="hand2")
    link_cdb.grid(row=5, column=0)
    link_cdb.bind("<Button-1>", lambda e: describe_cdb())

    link_lca = tk.Label(frame, text="LCA", fg="blue", cursor="hand2")
    link_lca.grid(row=5, column=1)
    link_lca.bind("<Button-1>", lambda e: describe_lca())

    link_lci = tk.Label(frame, text="LCI", fg="blue", cursor="hand2")
    link_lci.grid(row=5, column=2)
    link_lci.bind("<Button-1>", lambda e: describe_lci())

    link_tesouro = tk.Label(frame, text="Tesouro Direto", fg="blue", cursor="hand2")
    link_tesouro.grid(row=5, column=3)
    link_tesouro.bind("<Button-1>", lambda e: describe_tesouro_direto())

    # Linha 7: Botões
    button_investimentos = tk.Button(frame, text="Investimentos", command=go_investments)
    button_investimentos.grid(row=6, column=0, pady=(10,5))

    button_saque = tk.Button(frame, text="Saque", command=go_withdraw)
    button_saque.grid(row=6, column=1, pady=(10,5))

    button_investir = tk.Button(frame, text="Investir", command=go_invest)
    button_investir.grid(row=6, column=2, pady=(10,5))

    button_depositar = tk.Button(frame, text="Depositar", command=go_deposit)
    button_depositar.grid(row=6, column=3, pady=(10,5))

    root.mainloop()

if __name__ == "__main__":
    show_home_screen()
