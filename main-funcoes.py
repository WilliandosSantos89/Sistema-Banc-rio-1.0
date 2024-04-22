import textwrap

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
    print(f'\nSadlo:\t\tR$ {saldo/:.2f}')
    print('===================================')

def criar_usuário(usuarios):
    cpf: input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n@@@ Já existe um usuário com esse CPF! @@@')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = ('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado: )')

    usuarios.append({'nome': nome,'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print(' ==== Usuário criado com sucesso! ====')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuarios if usuario['cpf']== cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF  do usuários: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n=== Conta criada com sucesso! ===')
        return{'agencia'= agencia, 'numero_conta'= numero_conta, 'usuario'= usuario}

    print('@@@ Usuário não encontrado! Fluxo de criação de conta errado. @@@')

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
                Agência:\t{conta['agencia']}
                CC:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))