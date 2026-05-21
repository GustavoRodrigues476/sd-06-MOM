# SD-02 — Threads Distribuídas com Python

Exemplo de sistema distribuído utilizando **threads** com `threading` do Python, comunicando-se entre duas máquinas virtuais Linux via **sockets TCP**.

---

## Descritivo do Programa

**O que é?**
Um sistema distribuído onde o client envia ao server o modo de sincronização desejado e o server executa 4 threads em paralelo usando esse modo, retornando os resultados ao client.

**Como funciona?**
O server aguarda conexão na porta 5001. Ao receber os parâmetros do client (modo e configurações), cria 4 threads que executam uma contagem em paralelo. Dependendo do modo escolhido, as threads acessam a seção crítica de formas diferentes — sem controle, com Lock, com Semáforo(1) ou com Semáforo(2). Os resultados são coletados e enviados de volta ao client.

**Por que isso é distribuído?**
O processamento e a sincronização das threads acontecem no server (VM 1), enquanto o client (VM 2) controla remotamente qual modo de sincronização será usado e recebe os resultados, caracterizando a divisão de responsabilidades entre máquinas distintas em uma rede.

**Os 4 modos demonstrados**
- `simples` — threads sem sincronização, saída intercalada e imprevisível
- `lock` — `threading.Lock()` garante que apenas 1 thread por vez acessa a seção crítica
- `semaforo1` — `threading.Semaphore(1)` equivalente ao Lock, 1 thread por vez
- `semaforo2` — `threading.Semaphore(2)` permite 2 threads simultâneas na seção crítica

**Tecnologias utilizadas**
- `threading.Thread` — criação de threads paralelas
- `threading.Lock` — exclusão mútua entre threads
- `threading.Semaphore` — controle de acesso com limite configurável
- `socket TCP` — comunicação entre as duas máquinas virtuais
- `Vagrant + VirtualBox` — provisionamento das VMs Linux

---

## Arquitetura

```
┌─────────────────────┐        socket TCP         ┌──────────────────────────────┐
│   CLIENT VM         │ ────────────────────────> │   SERVER VM                  │
│   192.168.56.11     │   envia modo + params     │   192.168.56.10              │
│                     │ <──────────────────────── │                              │
│   client.py         │   recebe resultados       │   server.py                  │
└─────────────────────┘                           │   ├── Thread 1               │
                                                  │   ├── Thread 2               │
                                                  │   ├── Thread 3               │
                                                  │   └── Thread 4               │
                                                  │   sincronização: Lock/Sem    │
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
sd-02-threads/
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
git clone https://github.com/GustavoRodrigues476/sd-02-threads
cd sd-02-threads
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
# Executa todos os modos em sequência
vagrant ssh client
python3 /vagrant/src/client.py

# Ou escolha um modo específico
python3 /vagrant/src/client.py simples
python3 /vagrant/src/client.py lock
python3 /vagrant/src/client.py semaforo1
python3 /vagrant/src/client.py semaforo2
```

---

## Saída esperada

**Modo simples** — threads se intercalam sem ordem definida:
```
[Thread 2] (sem sincronização) n=40000 | i=0
[Thread 1] (sem sincronização) n=10000 | i=0
[Thread 3] (sem sincronização) n=90000 | i=0
[Thread 4] (sem sincronização) n=160000 | i=0
```

**Modo lock** — uma thread por vez na seção crítica:
```
[Thread 1] Aguardando Lock...
[Thread 2] Aguardando Lock...
[Thread 3] Aguardando Lock...
[Thread 4] Aguardando Lock...
[Thread 1] Lock ADQUIRIDO
[Thread 1] (lock) n=10000 | i=0
[Thread 1] (lock) n=10000 | i=1
[Thread 1] Lock LIBERADO
[Thread 2] Lock ADQUIRIDO
...
```

**Modo semaforo2** — duas threads simultâneas:
```
[Thread 1] Semáforo(2) ADQUIRIDO
[Thread 2] Semáforo(2) ADQUIRIDO
[Thread 1] (semaforo2) n=10000 | i=0
[Thread 2] (semaforo2) n=40000 | i=0
[Thread 1] Semáforo(2) LIBERADO
[Thread 3] Semáforo(2) ADQUIRIDO
...
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