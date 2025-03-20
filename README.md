# Cristian's Algorithm

Este repositório contém uma implementação do **Algoritmo de Cristian**, desenvolvido como parte da disciplina de Sistemas Distribuídos na **Universidade Federal de Ouro Preto**.

## Sobre o Algoritmo de Cristian

O Algoritmo de Cristian é um método utilizado para sincronização de relógios em sistemas distribuídos. Ele permite que um cliente ajuste seu relógio com base no tempo fornecido por um servidor central, minimizando as discrepâncias temporais entre os nós do sistema.

Esta implementação foi desenvolvida para funcionar em sistemas **Windows**, utilizando a biblioteca `pywin32` para ajustar o horário do sistema.

## Como Executar

Para executar a implementação, siga os passos abaixo:

### Pré-requisitos

1. **Python 3**:
   - Certifique-se de que o Python 3 está instalado no seu sistema. Você pode verificar isso executando:
     ```bash
     python --version
     ```
   - Caso não tenha o Python instalado, baixe e instale a partir do site oficial: [python.org](https://www.python.org/).

2. **Bibliotecas Necessárias**:
   - Instale as bibliotecas necessárias executando o seguinte comando no terminal:
     ```bash
     pip install ntplib python-dateutil pywin32
     ```

3. **Permissões de Administrador**:
   - No Windows, o cliente precisa ser executado com permissões de administrador para ajustar o horário do sistema. Certifique-se de abrir o terminal como administrador ao executar o cliente.

---

### Passos para Execução

1. **Servidor**:

   - Abra um terminal e navegue até o diretório do projeto.
   - Execute o servidor utilizando o comando:
     ```bash
     python server.py
     ```
   - O servidor estará ativo e aguardando conexões dos clientes.

2. **Cliente**:

   - Abra um **novo terminal como administrador**:
     - No Windows, pesquise por "Command Prompt" ou "PowerShell" no menu Iniciar.
     - Clique com o botão direito e selecione **"Executar como administrador"**.
   - Navegue até o diretório do projeto.
   - Execute o cliente utilizando o comando:
     ```bash
     python client.py
     ```
   - O cliente se conectará ao servidor, ajustará o horário do sistema e exibirá métricas de latência e diferença de sincronização.

3. **Múltiplos Clientes**:

   - Para simular múltiplos dispositivos, abra vários terminais como administrador e execute o cliente em cada um deles.
   - Cada cliente se conectará ao servidor e ajustará seu relógio de forma independente.

---

### Estrutura do Projeto

- **server.py**: Contém a implementação do servidor, que consulta o horário do NTP e envia para os clientes.
- **client.py**: Contém a implementação do cliente, que ajusta o horário do sistema com base no horário recebido do servidor.
- **log_servidor.txt**: Arquivo de log gerado pelo servidor, registrando as conexões e horários enviados.
- **log_sincronizacao.txt**: Arquivo de log gerado pelo cliente, registrando as métricas de latência e diferença de sincronização.

---

### Observações

- **Permissões de Administrador**: No Windows, o cliente precisa ser executado como administrador para ajustar o horário do sistema. Caso contrário, ocorrerá um erro de permissão.
- **Fuso Horário**: O servidor envia o horário no formato UTC. O cliente converte o horário para o fuso horário local antes de ajustar o sistema.
- **Logs**: Os logs são salvos nos arquivos `log_servidor.txt` e `log_sincronizacao.txt` para facilitar a análise e depuração.

---

### Exemplo de Saída

#### Servidor:

Servidor ativo e aguardando conexões...
Conexão estabelecida com ('127.0.0.1', 54321)
Horário enviado ao cliente ('127.0.0.1', 54321): 2025-03-20 20:55:30.273088+00:00
Conexão com ('127.0.0.1', 54321) encerrada.


#### Cliente:

Iteração: 1
Horário recebido do servidor: 2025-03-20 20:55:30.273088+00:00
Latência: 0.037462 segundos
Horário ajustado: 2025-03-20 20:55:30.291819+00:00
Diferença de sincronização: 0.018331 segundos


