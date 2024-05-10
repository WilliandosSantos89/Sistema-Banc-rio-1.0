import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.regristrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

        @classmethod
        def nova_conta(cls, cliente, numero):
            return cls(numero, cliente)
        
        @property
        def saldo(self):
            return self._saldo
        
        @property
        def numero(self):
            return self._numero
        
        @property
        def agenca(self):
            return self._agencia
        
        @property
        def cliente(self):
            return self._cliente
        
        @property
        def historico(self):
            return self._historico
        
        def sacar(self, valor):
            saldo = self.saldo
            excedeu_saldo = valor > saldo

            if excedeu_saldo:
                print('\n@@@ Operação Falhou! Você não tem saldo suficiente. @@@')

            elif valor > 0:
                self._saldo -= valor
                print('\n=== Saque realizado com sucesso. === ')                
                return True
            
            else: 
                print('\n@@@ Operação falhou! O valor informado é inválido. @@@')

            return False
        
        def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                print('\n=== Depósito realizado com sucesso! ===')

            else:
                print('\n@@@ Operação falhou! O valor informado é inválido. @@@')


class ContaCorrete(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacos if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('\n@@@ Operação falhou! O valor do saque excede o limite. @@@')

        elif excedeu_saques:
            print('\n@@@ Operação falhou. Número máximo de saques excedidos. @@@')

        else:
             return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/C:\t\t{self.numero}
            Titular\t{self.cliente.nome}
        """
    

class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%s')
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ==============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n@@@ Cliente não possui conta. @@@')
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    valor = float(input('Quanto você quer depositar? : '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(cliente):
    cpf = input('Informe o CPF do clinte: ')
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')

        valor = float(input('Quanto você quer sacar? :'))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrato! @@@')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print('\n=============== EXTRATO =============')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas transações.'

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f} ')
    print('=' * 20)

def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('@@@ Já existe um clinte com esse CPF! @@@')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereco (logradourom nro - bairro - cidade/sigla estado): ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n*** Cliente criado com sucesso! ****')

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('@@@ Cliente não encontrato, fluxo de criação de conta encerrado.')
        return
    
    conta = ContaCorrete.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n*** Conta Criada com sucesso! *** ')

def listar_contas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break

        else:
            print('\n@@@ Operação inválida, por favor, selecione outra opção. @@@')

main()

