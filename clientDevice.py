import sys
import datetime
import time
import socket
from dateutil import parser
from timeit import default_timer as timer

# Removido a importação do pywintypes e win32api, pois não são necessários no celular


def sincronizar_cliente():
    """
    Função principal do cliente para sincronizar o horário usando o Algoritmo de Cristian.
    """
    try:
        # Cria um socket para comunicação com o servidor
        sock = socket.socket()
        # Conecta ao servidor local na porta 8000
        sock.connect(('192.168.5.171', 8000))  # IP do servidor no notebook
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        return None, None  # Retorna valores nulos em caso de erro

    # Registra o momento de envio da requisição
    inicio_requisicao = timer()

    # Recebe o horário do servidor
    horario_servidor = parser.parse(sock.recv(1024).decode())

    # Registra o momento de recebimento da resposta
    fim_resposta = timer()

    # Horário atual do cliente antes da sincronização
    horario_atual_cliente = datetime.datetime.now()

    print(f"Horário recebido do servidor: {horario_servidor}")

    # Calcula a latência (tempo de ida e volta)
    latencia = fim_resposta - inicio_requisicao
    print(f"Latência: {latencia:.6f} segundos")

    # Ajusta o horário do cliente com base no horário do servidor e na latência
    horario_ajustado = horario_servidor + \
        datetime.timedelta(seconds=latencia / 2)

    # Remover fuso horário de ambos os horários (torná-los naive)
    horario_atual_cliente = horario_atual_cliente.replace(tzinfo=None)
    horario_ajustado = horario_ajustado.replace(tzinfo=None)

    # Atualiza o horário de forma gradual (exemplo de atualização de 10% do erro)
    erro = horario_ajustado - horario_atual_cliente
    ajuste_gradual = erro * 0.1  # Ajuste gradual de 10%

    # Apenas exibe o horário ajustado gradualmente (sem alterar o horário do sistema)
    print(
        f"Horário ajustado (gradualmente): {horario_atual_cliente + ajuste_gradual}")

    # Calcula a diferença entre o horário atual e o ajustado
    diferenca = abs(horario_atual_cliente -
                    (horario_atual_cliente + ajuste_gradual))
    print(
        f"Diferença de sincronização: {diferenca.total_seconds():.6f} segundos")

    sock.close()
    return latencia, diferenca.total_seconds()


def salvar_log(latencia, diferenca):
    """
    Função para salvar logs de sincronização em um arquivo.
    """
    with open("log_sincronizacao.txt", "a") as arquivo_log:
        arquivo_log.write(
            f"Latência: {latencia:.6f} segundos, Diferença: {diferenca:.6f} segundos\n")


if _name_ == '_main_':
    intervalo_minutos = 0.5  # Intervalo de sincronização em minutos
    iteracao = 1  # Contador de iterações
    latencia_total = 0
    diferenca_total = 0

    while True:
        print(f"Iteração: {iteracao}")
        latencia, diferenca = sincronizar_cliente()
        if latencia is not None and diferenca is not None:
            latencia_total += latencia
            diferenca_total += diferenca

            # Exibe as médias de latência e diferença de sincronização
            print(
                f"Média de latência: {latencia_total / iteracao:.6f} segundos")
            print(
                f"Média de diferença de sincronização: {diferenca_total / iteracao:.6f} segundos")
            print(
                "-------------------------------------------------------------------------------")

            # Salva os logs em um arquivo
            salvar_log(latencia, diferenca)

            iteracao += 1
        time.sleep(60 * intervalo_minutos)  # Aguarda o intervalo definido
