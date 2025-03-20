import sys
import datetime
import time
import socket
from dateutil import parser
from timeit import default_timer as timer

# Função para ajustar o horário do sistema no Windows
import win32api
import pywintypes

def atualizar_horario_sistema_windows(timestamp):
    """
    Função para ajustar o horário do sistema no Windows.
    """
    try:
        # Converte o timestamp para o formato adequado
        data_hora = (
            timestamp.year, timestamp.month, timestamp.weekday() + 1,  # Dia da semana (0=domingo, 1=segunda, etc.)
            timestamp.day, timestamp.hour, timestamp.minute, timestamp.second,
            timestamp.microsecond // 1000  # Windows usa milissegundos
        )
        # Ajusta o horário do sistema
        win32api.SetSystemTime(*data_hora)
    except pywintypes.error as e:
        print(f"Erro ao ajustar o horário do sistema: {e}")

def atualizar_horario_sistema(timestamp):
    """
    Função para ajustar o horário do sistema, compatível com Linux e Windows.
    """
    if sys.platform.startswith('linux'):
        # Código para Linux
        try:
            import subprocess
            import shlex

            data_hora = (timestamp.year, timestamp.month, timestamp.day,
                         timestamp.hour, timestamp.minute, timestamp.second,
                         timestamp.microsecond)
            str_data_hora = datetime.datetime(*data_hora).isoformat()

            subprocess.call(shlex.split("sudo timedatectl set-ntp false"))
            subprocess.call(shlex.split(f"sudo date -s '{str_data_hora}'"))
            subprocess.call(shlex.split("sudo hwclock -w"))
        except Exception as e:
            print(f"Erro ao ajustar o horário do sistema: {e}")
    elif sys.platform.startswith('win32'):
        # Código para Windows
        atualizar_horario_sistema_windows(timestamp)
    else:
        print("Sistema operacional não suportado para ajuste de horário.")

def sincronizar_cliente():
    """
    Função principal do cliente para sincronizar o horário usando o Algoritmo de Cristian.
    """
    try:
        # Cria um socket para comunicação com o servidor
        sock = socket.socket()
        # Conecta ao servidor local na porta 8000
        sock.connect(('127.0.0.1', 8000))
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
    horario_ajustado = horario_servidor + datetime.timedelta(seconds=latencia / 2)

    # Converte o horario_ajustado para "offset-naive" (remove o fuso horário)
    horario_ajustado = horario_ajustado.replace(tzinfo=None)

    # Atualiza o horário do sistema (Windows ou Linux)
    atualizar_horario_sistema(horario_ajustado)

    print(f"Horário ajustado: {horario_ajustado}")

    # Calcula a diferença entre o horário atual e o ajustado
    diferenca = abs(horario_atual_cliente - horario_ajustado)
    print(f"Diferença de sincronização: {diferenca.total_seconds():.6f} segundos")

    sock.close()
    return latencia, diferenca.total_seconds()

def salvar_log(latencia, diferenca):
    """
    Função para salvar logs de sincronização em um arquivo.
    """
    with open("log_sincronizacao.txt", "a") as arquivo_log:
        arquivo_log.write(f"Latência: {latencia:.6f} segundos, Diferença: {diferenca:.6f} segundos\n")

if __name__ == '__main__':
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
            print(f"Média de latência: {latencia_total / iteracao:.6f} segundos")
            print(f"Média de diferença de sincronização: {diferenca_total / iteracao:.6f} segundos")
            print("-------------------------------------------------------------------------------")

            # Salva os logs em um arquivo
            salvar_log(latencia, diferenca)

            iteracao += 1
        time.sleep(60 * intervalo_minutos)  # Aguarda o intervalo definido