import socket
import ntplib
from datetime import datetime, timezone
import threading


def obter_horario_ntp():
    """
    Obtém o horário atual de um servidor NTP.
    Retorna um objeto datetime com o horário obtido.
    """
    try:
        cliente_ntp = ntplib.NTPClient()
        resposta = cliente_ntp.request(
            'pool.ntp.org', version=3, timeout=5)  # Timeout de 5 segundos
        return datetime.fromtimestamp(resposta.tx_time, tz=timezone.utc)
    except Exception as e:
        print(f"Erro ao consultar o servidor NTP: {e}")
        # Retorna o horário local em caso de falha
        return datetime.now(timezone.utc)


def salvar_log(mensagem):
    """
    Função para salvar logs de atividade do servidor em um arquivo.
    """
    with open("log_servidor.txt", "a") as arquivo_log:
        arquivo_log.write(f"{datetime.now(timezone.utc)} - {mensagem}\n")


def tratar_cliente(conexao, endereco):
    """
    Função para tratar a conexão de um cliente.
    """
    try:
        # Obtém o horário atual do NTP
        horario_atual = obter_horario_ntp()
        print(f"Horário enviado ao cliente {endereco}: {horario_atual}")
        salvar_log(f"Horário enviado ao cliente {endereco}: {horario_atual}")

        # Envia o horário para o cliente
        conexao.send(str(horario_atual).encode())
    except Exception as e:
        print(f"Erro ao tratar o cliente {endereco}: {e}")
    finally:
        # Fecha a conexão com o cliente
        conexao.close()
        print(f"Conexão com {endereco} encerrada.")
        salvar_log(f"Conexão com {endereco} encerrada.")


def iniciar_servidor():
    """
    Inicia o servidor para sincronização de horário usando o Algoritmo de Cristian.
    """
    # Cria um socket para comunicação
    sock = socket.socket()

    # Associa o socket ao endereço e porta 8000
    sock.bind(('', 8000))

    # Coloca o servidor em modo de escuta
    sock.listen(5)
    print("Servidor ativo e aguardando conexões...")
    salvar_log("Servidor iniciado.")

    while True:
        # Aceita uma conexão de cliente
        conexao, endereco = sock.accept()
        print(f"Conexão estabelecida com {endereco}")
        salvar_log(f"Conexão estabelecida com {endereco}")

        # Cria uma thread para tratar o cliente
        threading.Thread(target=tratar_cliente,
                         args=(conexao, endereco)).start()


if __name__ == '__main__':
    iniciar_servidor()
