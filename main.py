#Sistema Bancário 1.0

#Variáveis globais
saldo_atual = 0
extrato = []

#Funções para as operações
def verificar_saldo():
    print('Seu saldo atual é de {:.2f}'.format(saldo_atual))

#Função para realizar saque
def realizar_saque(amount):
    global saldo_atual
    if amount <= saldo_atual: #O saque deve ser menor ou igual ao saldo atual
        saldo_atual -= amount #Saldo atual menos o saque
        extrato.append('Saque: {:.2f}'.format(extrato))
        print('Saque realizado com sucesso. Novo saldo {:.2f}'.format(saldo_atual))
    else:
        print('Saldo insuficiente.')

#Função para realizar depósitos
def realizar_deposito(amount):
    global saldo_atual
    saldo_atual += amount #Soma o saldo atual + depósito realizado
    extrato.append('Depósito: {:.2f}'.format(amount))
    print('Depósito realizado com sucesso. Novo saldo: {:.2f}'.format(saldo_atual))

#Função para mostrar o histórico de transações
def ver_historico_transacoes():
    print('\nHistórico de Transações:')
    for transacoes in extrato: #Cria uma variável para puxar o extrato
        print(transacoes)

#Menu principal
while True:
    print('\nBem vindo(a)\n')
    opcoes = input('Escolha uma das opções:\n')
    print('1. Verificar Saldo')
    print('2. Realizar Saque')
    print('3. Realizar Depósito')
    print('4. Ver Extrato')
    print('5. Sair')

    if opcoes == '1':
        


        





