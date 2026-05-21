# SD-03 — Sockets Distribuídos com Python

Exemplo de sistema distribuído utilizando **sockets TCP** do Python, comunicando-se entre duas máquinas virtuais Linux com suporte a **múltiplos clients simultâneos**.

---

## Descritivo do Programa

**O que é?**
Uma calculadora distribuída onde o client envia dois números e uma operação ao server via socket TCP, o server realiza o cálculo e retorna o resultado. O server suporta múltiplos clients simultâneos através de threads.

**Como funciona?**
O server aguarda conexões na porta 5000. A cada nova conexão, cria uma thread dedicada para atender aquele client, permitindo que vários clients se conectem ao mesmo tempo sem bloqueio. O client envia os dados no formato `X;Y;operacao`, o server interpreta o protocolo, executa a operação e devolve o resultado.

**Por que isso é distribuído?**
O processamento do cálculo acontece no server (VM 1), enquanto o client (VM 2) apenas envia os operandos e a operação desejada, recebendo somente o resultado. Cada client é identificado pelo seu IP e porta no log do server, evidenciando a comunicação entre máquinas distintas na rede.

**Operações disponíveis**
- `soma` — adição entre dois números
- `subtracao` — subtração entre dois números
- `multiplicacao` — multiplicação entre dois números
- `divisao` — divisão entre dois números (com tratamento de divisão por zero)
- `potencia` — x elevado a y
- `modulo` — resto da divisão de x por y

**Tecnologias utilizadas**
- `socket.AF_INET, socket.SOCK_STREAM` — socket TCP
- `threading.Thread` — múltiplos clients simultâneos
- Protocolo de comunicação com `;` separando os valores
- `Vagrant + VirtualBox` — provisionamento das VMs Linux

---

## Arquitetura

```
┌─────────────────────┐        socket TCP         ┌──────────────────────────────┐
│   CLIENT VM         │ ────────────────────────> │   SERVER VM                  │
│   192.168.56.11     │   envia: X;Y;operacao     │   192.168.56.10              │
│                     │ <──────────────────────── │                              │
│   client.py         │   recebe: resultado       │   server.py                  │
└─────────────────────┘                           │   ├── Thread client 1        │
                                                  │   ├── Thread client 2        │
                                                  │   └── Thread client N        │
                                                  └──────────────────────────────┘
```

---

## Pré-requisitos

- [VirtualBox 7.0.x](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0)
- [Vagrant](https://developer.hashicorp.com/vagrant/downloads)

> **Atenção:** VirtualBox 7.1.x pode apresentar problemas de compatibilidade com o Vagrant no Windows. Recomenda-se a versão **7.0.x**.

---

## Estrutura do projeto

```
sd-03-sockets/
├── Vagrantfile
├── README.md
├── .gitignore
├── setup/
│   ├── setup-server.sh
│   └── setup-client.sh
└── src/
    ├── server.py
    └── client.py
```

---

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoRodrigues476/sd-03-sockets
cd sd-03-sockets
```

### 2. Suba as VMs

```bash
vagrant up
```

> Na primeira execução o Vagrant baixa a imagem do Ubuntu (~500MB). Aguarde as duas VMs aparecerem como `ready`.

Se apenas uma VM subir, suba a outra manualmente:

```bash
vagrant up client
```

### 3. Abra dois terminais

**Terminal 1 — inicie o servidor:**

```bash
vagrant ssh server
python3 /vagrant/src/server.py
```

**Terminal 2 — execute o client:**

```bash
vagrant ssh client
python3 /vagrant/src/client.py
```

---

## Saída esperada

**Terminal do server:**
```
[Servidor] Aguardando conexões na porta 5000...
[Servidor] Operações disponíveis: soma, subtracao, multiplicacao, divisao, potencia, modulo
[Servidor] Client conectado: ('192.168.56.11', 54320)
[Servidor] Threads ativas: 1
[Servidor] 10.0 soma 5.0 = 15.0 | client: ('192.168.56.11', 54320)
[Servidor] Conexão encerrada: ('192.168.56.11', 54320)
[Servidor] Client conectado: ('192.168.56.11', 54321)
[Servidor] Threads ativas: 1
[Servidor] 10.0 subtracao 5.0 = 5.0 | client: ('192.168.56.11', 54321)
[Servidor] Conexão encerrada: ('192.168.56.11', 54321)
...
```

**Terminal do client:**
```
=== Calculadora Distribuída ===
Operações disponíveis: soma, subtracao, multiplicacao, divisao, potencia, modulo

--- SOMA ---
[Client] Enviando: 10;5;soma
[Client] Resultado: 15.0

--- SUBTRACAO ---
[Client] Enviando: 10;5;subtracao
[Client] Resultado: 5.0

--- MULTIPLICACAO ---
[Client] Enviando: 10;5;multiplicacao
[Client] Resultado: 50.0

--- DIVISAO ---
[Client] Enviando: 10;5;divisao
[Client] Resultado: 2.0

--- POTENCIA ---
[Client] Enviando: 2;8;potencia
[Client] Resultado: 256.0

--- MODULO ---
[Client] Enviando: 10;3;modulo
[Client] Resultado: 1.0
```

---

## Solução de problemas

### Erro: `timeout during server version negotiating`

Adicione as linhas abaixo no bloco `provider` de cada VM no `Vagrantfile`:

```ruby
vb.customize ["modifyvm", :id, "--usb", "off"]
vb.customize ["modifyvm", :id, "--usbehci", "off"]
```

Depois execute:

```bash
vagrant destroy -f
vagrant up
```

### Erro: `VM not created. Moving on...`

Suba a VM individualmente:

```bash
vagrant up client
```

### Erro de SSH agent

Adicione ao `Vagrantfile` logo após `Vagrant.configure("2") do |config|`:

```ruby
config.ssh.forward_agent = false
```

---

## Comandos úteis do Vagrant

```bash
vagrant up              # sobe as duas VMs
vagrant up server       # sobe só o server
vagrant up client       # sobe só o client
vagrant ssh server      # acessa o server via SSH
vagrant ssh client      # acessa o client via SSH
vagrant halt            # desliga as VMs (sem apagar)
vagrant destroy -f      # apaga as VMs
vagrant reload          # reinicia as VMs
vagrant reload --provision  # reinicia e roda os scripts de setup novamente
vagrant status          # exibe o status das VMs
```

---

## Disciplina

Sistemas Distribuídos
