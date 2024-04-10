#Sistema Bancário 1.0

#Variáveis globais
saldo_atual = 0
extrato = []
saques_diarios = 0

#Constantes para limites de saques diários
QUANTIDADE_SAQUE_DIARIO = 3
QUANTIDADE_SAQUE_VALOR = 500

#Funções para as operações
def verificar_saldo():
    print('Seu saldo atual é de {:.2f}'.format(saldo_atual))

#Função para realizar saque
def realizar_saque(amount):
    global saldo_atual, saques_diarios
    if saques_diarios >= QUANTIDADE_SAQUE_DIARIO: #
        print('Limite de saques excedido. Tente novamente amanhã')
        return
    if amount > QUANTIDADE_SAQUE_VALOR:
        print('O valor máximo de saque é de R$ {:.2f}'.format(QUANTIDADE_SAQUE_VALOR))
        return
    if amount <= saldo_atual:
        saldo_atual -= amount
        extrato.append('Saque realizado com sucesso. Novo saldo: R$ {:.2f}'.format(saldo_atual))
    

#Função para realizar depósitos
def realizar_deposito(amount):
    global saldo_atual
    saldo_atual += amount #Soma o saldo atual + depósito realizado
    extrato.append('Depósito: {:.2f}'.format(amount))
    print('Depósito realizado com sucesso. Novo saldo: R$ {:.2f}'.format(saldo_atual))

#Função para mostrar o histórico de transações
def ver_historico_transacoes():
    print('\nExtrato Detalhado:')
    for transacoes in extrato: #Cria uma variável para puxar o extrato
        print(transacoes)

#Menu principal
while True:
    print('\nBem vindo(a)')
    
    print('1. Verificar Saldo')
    print('2. Realizar Saque')
    print('3. Realizar Depósito')
    print('4. Ver Extrato')
    print('5. Sair')
    opcoes = input('Escolha uma das opções acima:\n')
    

    if opcoes == '1':
        verificar_saldo()
    elif opcoes == '2':
        saque_amount = float(input('Digite o valor a ser sacado: R$'))
        realizar_saque(saque_amount)
    elif opcoes == '3':
        deposito_amount = float(input('Digite o valor a ser depositado: R$'))
        realizar_deposito(deposito_amount)
    elif opcoes == '4':
        ver_historico_transacoes()
    elif opcoes == '5':
        print('Obrigado por ser nosso cliente. Até logo!')
        break
    else:
        print('Opção inválida. Escolha uma das opções de 1-5.')



        





