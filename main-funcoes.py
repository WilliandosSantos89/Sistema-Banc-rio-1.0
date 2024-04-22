import textwrap
from datetime import datetime

def menu():
    menu = """\n
    =========== MENU ===========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\tR$ {valor:.2f}\n'
        print('\n=== Depósito Realizado com Sucesso ===')
    else:
        print('\n@@@ Operação Falhou! O valor informado é inválido. @@@')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saldo:
        print('\n@@@ Operação Falhou! Você não tem saldo suficiente. @@@')

    elif excedeu_limite:
        print('@@@ Operação Falhou! O valor de saque excede o limite. @@@')

    elif excedeu_saques:
        print('@@@ Operação Falhou! Número máximo de saque excedido.')

    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: \t\tR$ {valor:.2f}\n'
        numero_saques += 1
        print('\n=== Saque realizado com sucesso! ===')

    else:
        print('@@@ Operação Falhou! O valor informado é inválido. @@@')

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):

    print('\n============ EXTRATO ============')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'\nSaldo:\t\tR$ {saldo:.2f}')
    print('===================================')

#Função para validar CPF
def validar_cpf(cpf):
    #Verifica se o CPF contém 11 dígitos
    return len(cpf) == 11 and cpf.isdigit()

#Função para validar data no formato dd-mm-aaaa
def validar_data(date_text):
    try:
        datetime.strptime(date_text, '%d-%m-%Y')
        return True
    except ValueError:
        return False
    
#Função para validar nome completo (pelo menos dois nomes)
def validar_nome(name):
    return len(name.split()) >= 2

#Função para validar endereço (não vazio e conter pelo menos duas vírgulas)
def validar_endereco(address):
    return len(address) > 0 and address.count(',') >= 2

#Função para criar usuários
def criar_usuário(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    if not validar_cpf(cpf):
        print('@@@ CPF inválido. Deve conter pelo menos 11 dígitos. @@@')
        return
    
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print('\n@@@ Já existe um usuário com esse CPF! @@@')
        return
    
    nome = input('Informe o nome completo: ')
    if not validar_nome(nome):
        print('@@@ Nome inválido. Deve conter pelo menos dois nomes. @@@')
        return

    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    if not validar_data(data_nascimento):
        print('@@@ Data de nascimento inválida. Deve ser no formato dd-mm-aaaa @@@')
        return

    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado: )')
    if not validar_endereco(endereco):
        print('@@@ Endereço incompleto. Separe por vírgula. @@@')
        return

    usuarios.append({'nome': nome,'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print(' ==== Usuário criado com sucesso! ====')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf']== cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF  do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n=== Conta criada com sucesso! ===')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}

    print('\n@@@ Usuário não encontrado! Fluxo de criação de conta errado. @@@')

def listar_contas(contas):


    for conta in contas:
        linha = f"""\
                Agência:\t{conta['agencia']}
                CC:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input('Informe o valor do depósito: R$ '))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input('Informe o valor do saque: R$ '))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'nu':
            criar_usuário(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break

        else: 
            print('Opção inválida, por favor selecione novamente a opção desejada.')

main()