class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:
    LIMITE_SAQUES = 3
    LIMITE_DEPOSITO = 500  # Exemplo de limite de depósito

    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.extrato = ""
        self.numero_saques = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > Conta.LIMITE_DEPOSITO
        excedeu_saques = self.numero_saques >= Conta.LIMITE_SAQUES

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        else:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia = '0001'
        self.numero_conta = 1

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        if any(usuario.cpf == cpf for usuario in self.usuarios):
            print("CPF já cadastrado. Cadastro falhou.")
            return

        novo_cliente = Cliente(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_cliente)
        print("Usuário cadastrado com sucesso.")

    def criar_conta_bancaria(self, cpf):
        cliente_encontrado = next((c for c in self.usuarios if c.cpf == cpf), None)
        
        if cliente_encontrado:
            nova_conta = Conta(self.agencia, self.numero_conta, cliente_encontrado)
            self.contas.append(nova_conta)
            print(f"Conta criada com sucesso. Número da conta: {self.numero_conta}")
            self.numero_conta += 1
        else:
            print("Usuário não encontrado. Cadastro de conta falhou.")

    def obter_conta(self, numero_conta):
        return next((c for c in self.contas if c.numero_conta == numero_conta), None)

# Menu principal
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar usuário
[b] Criar conta bancária
[q] Sair
=> """

banco = Banco()

# Loop principal
while True:
    opcao = input(menu)

    if opcao == "d":
        numero_conta = int(input("Informe o número da conta: "))
        valor = float(input("Informe o valor do depósito: "))
        conta = banco.obter_conta(numero_conta)
        if conta:
            conta.depositar(valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "s":
        numero_conta = int(input("Informe o número da conta: "))
        valor = float(input("Informe o valor do saque: "))
        conta = banco.obter_conta(numero_conta)
        if conta:
            conta.sacar(valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "e":
        numero_conta = int(input("Informe o número da conta: "))
        conta = banco.obter_conta(numero_conta)
        if conta:
            conta.exibir_extrato()
        else:
            print("Conta não encontrada.")

    elif opcao == "c":
        nome = input("Nome do usuário: ")
        data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        cpf = input("CPF (somente números): ")
        endereco = input("Endereço (logradouro . nro - bairro - cidade/sigla estado): ")
        banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao == "b":
        cpf = input("Informe o CPF do usuário para criar a conta: ")
        banco.criar_conta_bancaria(cpf)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
