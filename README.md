
# Sincronização de Horário - Algoritmo de Cristian

Este projeto implementa o **Algoritmo de Cristian** para sincronização de horários entre um servidor e um cliente em uma rede local. O servidor usa o protocolo NTP (Network Time Protocol) para obter o horário exato e enviá-lo ao cliente. O cliente calcula a latência e ajusta seu horário local com base no horário recebido do servidor.

## Estrutura do Projeto

- **client.py**: Código do cliente responsável por se conectar ao servidor e sincronizar seu horário com base no horário fornecido pelo servidor.
- **server.py**: Código do servidor que fornece o horário NTP para os clientes.
- **clientDevice.py**: Versão do código cliente para execução no dispositivo móvel usando Termux.

## Requisitos

- **Python 3.x**
- **Bibliotecas**:
  - `ntplib` (para interação com servidores NTP)
  - `python-dateutil` (para manipulação de datas)
  - `timeit` (para medir o tempo de latência)
  - `pywin32` (vínculo python e Windows)
  
### Instalando as Bibliotecas no Termux

No seu dispositivo Android com Termux, instale o Python e as bibliotecas necessárias com os seguintes comandos:

```bash
pkg install python
pip install ntplib python-dateutil
pip install pywin32
```

## Como Executar

### 1. Executando o Servidor (server.py)

O servidor escuta na porta `8000` e envia o horário NTP para os clientes que se conectam a ele.

1. Abra o Termux e navegue até o diretório onde o `server.py` está localizado.
2. Execute o servidor com o seguinte comando:

```bash
python server.py
```

O servidor ficará aguardando conexões de clientes.

### 2. Executando o Cliente (client.py ou clientDevice.py)

O cliente se conecta ao servidor e sincroniza seu horário com base no horário recebido.

1. No **Notebook** ou **Termux (dispositivo móvel)**, abra o arquivo `client.py` (ou `clientDevice.py` no Termux).
2. Execute o cliente com o seguinte comando:

```bash
python clientDevice.py
```

Isso iniciará a sincronização do horário. O cliente calculará a latência e ajustará seu horário local (sem alterar o horário do sistema no celular). O log será salvo no arquivo `log_sincronizacao.txt`.

### Configuração de Rede

Certifique-se de que o **servidor e os clientes** estão na mesma rede Wi-Fi local. O servidor usa o IP `192.168.5.171` (ou o IP do servidor local) para que os clientes se conectem.

### Log de Sincronização

A cada execução, o cliente salva as latências e diferenças de sincronização no arquivo `log_sincronizacao.txt`, o que pode ser útil para depuração e análise de desempenho.

### Exemplo de Log:

```text
Latência: 0.060939 segundos, Diferença: 0.001234 segundos
Média de latência: 0.060939 segundos
Média de diferença de sincronização: 0.001234 segundos
-------------------------------------------------------------------------------
```

## Estrutura do Código

### server.py

- **Função `obter_horario_ntp()`**: Obtém o horário atual de um servidor NTP.
- **Função `tratar_cliente()`**: Trata a conexão com o cliente e envia o horário NTP.
- **Função `iniciar_servidor()`**: Inicia o servidor e espera por conexões de clientes.

### client.py (ou clientDevice.py)

- **Função `sincronizar_cliente()`**: Conecta-se ao servidor e calcula a latência, ajustando o horário local com base no horário do servidor.
- **Função `salvar_log()`**: Salva as informações de latência e diferença de sincronização no arquivo de log.

## Considerações Finais

Este projeto é uma implementação básica do **Algoritmo de Cristian** em um ambiente de rede local. Ele pode ser adaptado para redes maiores ou para melhorar a precisão da sincronização.

**Limitações**:
- O **ajuste do horário do sistema** não é realizado no cliente em dispositivos móveis, apenas o cálculo e exibição da diferença.
- A **sincronização é feita periodicamente**, mas o código não garante precisão absoluta em redes com alta latência.
