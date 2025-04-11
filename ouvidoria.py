import mysql.connector  # Biblioteca para conectar com o banco de dados MySQL

# Conexão com o banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",         # Endereço do servidor do banco de dados (localhost = sua máquina)
    user="root",              # Nome de usuário do MySQL (padrão é root)
    password="1234",   # Senha que você cadastrou no MySQL
    database="ouvidoria"      # Nome do banco de dados (tem que estar criado antes)
)
cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL

# Cria a tabela de manifestações se ela ainda não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS manifestacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,     # ID único que aumenta automaticamente
    tipo VARCHAR(50) NOT NULL,             # Tipo da manifestação
    titulo VARCHAR(100) NOT NULL,          # Título ou nome da manifestação
    descricao TEXT NOT NULL                # Descrição da manifestação
)
""")
conexao.commit()  # Salva as alterações no banco

opcao = 0  # Variável de controle para o menu

while opcao != 7:
    # Exibe o menu
    print("\n 1) Listagem das Manifestações\n 2) Listagem por Tipo\n 3) Nova Manifestação\n 4) Quantidade\n 5) Buscar por Código\n 6) Excluir Manifestação\n 7) Sair")

    try:
        opcao = int(input("Digite sua opção: "))  # Lê a opção do usuário
    except ValueError:
        print("Digite um número válido!")
        continue

    if opcao == 1:
        cursor.execute("SELECT * FROM manifestacoes") # Me dê todas as colunas da tabela manifestações
        manifestacoes = cursor.fetchall()
        if not manifestacoes:
            print("Não existem manifestações cadastradas.")
        else:
            for m in manifestacoes:
                print(f"Código: {m[0]} | Tipo: {m[1].capitalize()} | Título: {m[2]} | Descrição: {m[3]}")

    elif opcao == 2:
        tipo = input("Digite o tipo de manifestação (reclamação, sugestão ou elo-gio): ").strip().lower()
        cursor.execute("SELECT * FROM manifestacoes WHERE tipo = %s", (tipo,)) # Me dê todas as colunas da tabela manifestações onde o tipo for igual a placeholder str
        manifestacoes = cursor.fetchall()
        if not manifestacoes:
            print(f"Não existem manifestações do tipo '{tipo}'.")
        else:
            for m in manifestacoes:
                print(f"Código: {m[0]} | Tipo: {m[1].capitalize()} | Título: {m[2]} | Descrição: {m[3]}")

    elif opcao == 3:
        tipo = input("Tipo da manifestação (reclamação, sugestão ou elogio): ").strip().lower()
        titulo = input("Título da manifestação: ").strip()
        descricao = input("Descrição da manifestação: ").strip()

        if not tipo or not titulo or not descricao:
            print("Todos os campos são obrigatórios!")
        else:
            cursor.execute("INSERT INTO manifestacoes (tipo, titulo, descricao) VALUES (%s, %s, %s)",
                           (tipo, titulo, descricao))
            conexao.commit()
            print("Nova manifestação criada com sucesso!")

    elif opcao == 4:
        cursor.execute("SELECT COUNT(*) FROM manifestacoes")
        quantidade = cursor.fetchone()[0]
        print(f"Quantidade total de manifestações: {quantidade}")

    elif opcao == 5:
        try:
            codigo = int(input("Digite o código da manifestação: "))
            cursor.execute("SELECT * FROM manifestacoes WHERE id = %s", (codigo,))
            m = cursor.fetchone()
            if m:
                print(f"Código: {m[0]} | Tipo: {m[1].capitalize()} | Título: {m[2]} | Descrição: {m[3]}")
            else:
                print("Manifestação não encontrada.")
        except ValueError:
            print("Digite um código válido.")

    elif opcao == 6:
        try:
            codigo = int(input("Digite o código da manifestação que deseja excluir: "))
            cursor.execute("SELECT * FROM manifestacoes WHERE id = %s", (codigo,))
            if cursor.fetchone():
                cursor.execute("DELETE FROM manifestacoes WHERE id = %s", (codigo,))
                conexao.commit()
                print("Manifestação excluída com sucesso!")
            else:
                print("Código não encontrado.")
        except ValueError:
            print("Digite um código válido.")

    elif opcao != 7:
        print("Opção inválida. Tente novamente.")

# Encerra a conexão com o banco e finaliza o programa
cursor.close()
conexao.close()
print("Sistema encerrado. Obrigada por usar a melhor ouvidoria de todas! <3")
