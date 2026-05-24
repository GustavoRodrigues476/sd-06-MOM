# SD-06 — MOM (Message-Oriented Middleware) com RabbitMQ

Exemplo de sistema distribuído utilizando **MOM (Message-Oriented Middleware)** com **RabbitMQ**, comunicando-se entre três máquinas virtuais Linux.

---

## Descritivo do Programa

**O que é?**
Um sistema de processamento de pedidos de e-commerce distribuído, onde o produtor envia pedidos ao broker (RabbitMQ) e o consumidor os processa de forma assíncrona. O broker garante que nenhuma mensagem seja perdida mesmo que o consumidor esteja offline.

**Como funciona?**
O broker (VM 1) roda o RabbitMQ Server e gerencia a fila `pedidos`. O produtor (VM 2) conecta ao broker via `pika`, declara a fila e publica pedidos em formato JSON com `basic_publish`. As mensagens são marcadas como persistentes (`delivery_mode=2`), garantindo que sobrevivam a uma reinicialização do broker. O consumidor (VM 3) conecta ao broker, declara a mesma fila e fica aguardando mensagens com `basic_consume`. A cada pedido recebido, processa e confirma o recebimento com `basic_ack`.

**Por que isso é distribuído?**
O produtor e o consumidor nunca se comunicam diretamente — eles nem sabem da existência um do outro. Toda a comunicação passa pelo broker. Isso demonstra o desacoplamento no tempo: o consumidor pode estar offline quando o produtor envia os pedidos, e os receberá assim que reconectar. É possível também ter múltiplos produtores e consumidores sem alterar nenhum código.

**Diferença para Sockets e RPC**
Em Sockets (SD-03) e RPC (SD-04), a comunicação é síncrona — o client espera a resposta do server. Com MOM, a comunicação é assíncrona — o produtor publica e segue em frente, sem esperar o consumidor processar. O broker é o intermediário que desacopla os dois lados.

**Tecnologias utilizadas**
- `RabbitMQ` — broker de mensagens AMQP
- `pika` — biblioteca Python para conectar ao RabbitMQ
- `queue_declare` com `durable=True` — fila persistente
- `basic_publish` com `delivery_mode=2` — mensagem persistente
- `basic_consume` + `basic_ack` — consumo com confirmação
- `Vagrant + VirtualBox` — provisionamento das VMs Linux

---

## Arquitetura

```
┌─────────────────────┐                      ┌─────────────────────┐
│   PRODUTOR VM       │                      │   CONSUMIDOR VM     │
│   192.168.56.11     │                      │   192.168.56.12     │
│                     │                      │                     │
│   produtor.py       │                      │   consumidor.py     │
└────────┬────────────┘                      └──────────┲──────────┘
         │ publica pedidos                   consome pedidos │
         │                                                   │
         └──────────────→ ┌──────────────────┐ ─────────────┘
                          │   BROKER VM      │
                          │   192.168.56.10  │
                          │   RabbitMQ       │
                          │   porta 5672     │
                          │   fila: pedidos  │
                          └──────────────────┘
```

---

## Pré-requisitos

- [VirtualBox 7.0.x](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0)
- [Vagrant](https://developer.hashicorp.com/vagrant/downloads)

> **Atenção:** VirtualBox 7.1.x pode apresentar problemas de compatibilidade com o Vagrant no Windows. Recomenda-se a versão **7.0.x**.

---

## Estrutura do projeto

```
sd-06-mom/
├── Vagrantfile
├── README.md
├── .gitignore
├── setup/
│   ├── setup-broker.sh
│   ├── setup-produtor.sh
│   └── setup-consumidor.sh
└── src/
    ├── produtor.py
    └── consumidor.py
```

---

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoRodrigues476/sd-06-mom
cd sd-06-mom
```

### 2. Suba as VMs

```bash
vagrant up
```

> Na primeira execução o Vagrant baixa a imagem do Ubuntu (~500MB) e instala o RabbitMQ e o `pika` automaticamente. A VM do broker pode demorar um pouco mais por instalar o RabbitMQ. Aguarde as três VMs aparecerem como `ready`.

Se alguma VM não subir, suba individualmente:

```bash
vagrant up broker
vagrant up consumidor
vagrant up produtor
```

### 3. Abra três terminais

**Terminal 1 — verifique o broker:**

```bash
vagrant ssh broker
sudo systemctl status rabbitmq-server
```

**Terminal 2 — inicie o consumidor (antes do produtor):**

```bash
vagrant ssh consumidor
python3 /vagrant/src/consumidor.py
```

**Terminal 3 — execute o produtor:**

```bash
vagrant ssh produtor
python3 /vagrant/src/produtor.py
```

> **Importante:** inicie o consumidor antes do produtor para ver as mensagens sendo processadas em tempo real. Se iniciar o produtor primeiro, as mensagens ficam na fila do broker e serão entregues assim que o consumidor conectar.

---

## Saída esperada

**Terminal do produtor:**
```
[Produtor] Conectado ao broker 192.168.56.10
[Produtor] Enviando 5 pedidos...

[Produtor] Pedido enviado: #A1B2C3D4 | Notebook Dell       | R$3500.00
[Produtor] Pedido enviado: #E5F6G7H8 | Mouse Logitech      | R$179.80
[Produtor] Pedido enviado: #I9J0K1L2 | Teclado Mecânico    | R$299.90
[Produtor] Pedido enviado: #M3N4O5P6 | Monitor LG 24"      | R$1200.00
[Produtor] Pedido enviado: #Q7R8S9T0 | Headset Sony        | R$450.00

[Produtor] Todos os pedidos enviados ao broker.
```

**Terminal do consumidor:**
```
[Consumidor] Conectado ao broker 192.168.56.10
[Consumidor] Aguardando pedidos... (CTRL+C para sair)

[Consumidor] Pedido recebido:
  ID:        #A1B2C3D4
  Produto:   Notebook Dell
  Qtd:       1
  Valor:     R$3500.00
  Total:     R$3500.00
  Hora:      10:32:15
[Consumidor] Processando...
[Consumidor] Pedido #A1B2C3D4 confirmado!

[Consumidor] Pedido recebido:
  ID:        #E5F6G7H8
  Produto:   Mouse Logitech
  ...
```

---

## Teste de desacoplamento no tempo

Uma das características mais importantes do MOM é o desacoplamento no tempo. Para demonstrar:

**1. Inicie o consumidor e depois pare:**
```bash
# Terminal 2
vagrant ssh consumidor
python3 /vagrant/src/consumidor.py
# Pressione CTRL+C para parar
```

**2. Com o consumidor offline, envie os pedidos:**
```bash
# Terminal 3
vagrant ssh produtor
python3 /vagrant/src/produtor.py
```

**3. Religue o consumidor:**
```bash
# Terminal 2
python3 /vagrant/src/consumidor.py
```

Os pedidos que ficaram na fila do broker serão entregues imediatamente ao consumidor assim que ele reconectar — sem perda de mensagens.

---

## Interface web do RabbitMQ

O RabbitMQ possui uma interface web para monitorar filas e conexões em tempo real. Acesse pelo navegador do Windows:

```
http://192.168.56.10:15672
Usuário: meuapp
Senha:   senha123
```

Na aba **Queues** você verá a fila `pedidos` com o contador de mensagens. Na aba **Connections** verá as conexões do produtor e consumidor.

---

## Solução de problemas

### Erro: `Connection refused` ao conectar no broker

Verifique se o RabbitMQ está rodando e escutando em todas as interfaces:

```bash
vagrant ssh broker
sudo systemctl status rabbitmq-server
sudo ss -tlnp | grep 5672
```

Deve aparecer `0.0.0.0:5672`. Se aparecer `127.0.0.1:5672`, force o provisionamento:

```bash
vagrant reload --provision broker
```

### Erro: `ACCESS_REFUSED`

O usuário `meuapp` não foi criado. Execute manualmente:

```bash
vagrant ssh broker
sudo rabbitmqctl add_user meuapp senha123
sudo rabbitmqctl set_user_tags meuapp administrator
sudo rabbitmqctl set_permissions -p / meuapp ".*" ".*" ".*"
```

### Erro: `ModuleNotFoundError: No module named 'pika'`

```bash
vagrant ssh produtor
pip3 install pika

vagrant ssh consumidor
pip3 install pika
```

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

---

## Comandos úteis do Vagrant

```bash
vagrant up              # sobe as três VMs
vagrant up broker       # sobe só o broker
vagrant up produtor     # sobe só o produtor
vagrant up consumidor   # sobe só o consumidor
vagrant ssh broker      # acessa o broker via SSH
vagrant ssh produtor    # acessa o produtor via SSH
vagrant ssh consumidor  # acessa o consumidor via SSH
vagrant halt            # desliga as VMs (sem apagar)
vagrant destroy -f      # apaga as VMs
vagrant reload          # reinicia as VMs
vagrant reload --provision  # reinicia e roda os scripts de setup novamente
vagrant status          # exibe o status das VMs
```

---

## Disciplina

Sistemas Distribuídos
