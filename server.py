import socket
import ntplib
from datetime import datetime, timezone


def obter_horario_ntp():
    """
    Obtém o horário atual de um servidor NTP.
    Retorna um objeto datetime com o horário obtido.
    """
    try:
        cliente_ntp = ntplib.NTPClient()
        resposta = cliente_ntp.request('pool.ntp.org', version=3)
        return datetime.fromtimestamp(resposta.tx_time, tz=timezone.utc)
    except Exception as e:
        print(f"Erro ao consultar o servidor NTP: {e}")
        # Retorna o horário local em caso de falha
        return datetime.now(timezone.utc)


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

    while True:
        # Aceita uma conexão de cliente
        conexao, endereco = sock.accept()
        print(f"Conexão estabelecida com {endereco}")

        try:
            # Obtém o horário atual do NTP
            horario_atual = obter_horario_ntp()
            print(f"Horário enviado ao cliente: {horario_atual}")
        except Exception as e:
            print(f"Erro ao obter o horário: {e}")
            # Usa o horário local em caso de erro
            horario_atual = datetime.now(timezone.utc)

        # Envia o horário para o cliente
        conexao.send(str(horario_atual).encode())

        # Fecha a conexão com o cliente
        conexao.close()
        print(f"Conexão com {endereco} encerrada.")


if __name__ == '__main__':
    iniciar_servidor()
