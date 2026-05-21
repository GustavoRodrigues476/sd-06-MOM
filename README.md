# SD-05 — Objetos Distribuídos com Python

Exemplo de sistema distribuído utilizando **Objetos Distribuídos** com a biblioteca `Pyro5` do Python, comunicando-se entre três máquinas virtuais Linux.

---

## Descritivo do Programa

**O que é?**
Um sistema de cotações de bolsa de valores distribuído, onde o client manipula remotamente um objeto `Bolsa` que vive no server. O objeto mantém estado persistente entre as chamadas — preços, carteira e histórico de operações são preservados enquanto o server estiver rodando.

**Como funciona?**
O Name Server (VM 1) atua como serviço de descoberta — o server registra o objeto com o nome `bolsa` e o client o localiza pelo nome sem precisar conhecer o IP do server diretamente. O server (VM 2) instancia o objeto `Bolsa`, decora a classe com `@Pyro5.api.expose` para tornar seus métodos acessíveis remotamente e registra o objeto no Name Server. O client (VM 3) conecta ao Name Server, obtém a referência do objeto e o utiliza como se fosse local.

**Por que isso é distribuído?**
O objeto `Bolsa` vive no server (VM 2), mas o client (VM 3) o manipula como se fosse uma instância local. O estado do objeto — preços atualizados, carteira e histórico — persiste entre chamadas e é compartilhado entre todos os clients conectados, demonstrando a transparência de localização característica dos objetos distribuídos.

**Diferença para RPC**
No RPC (SD-04), cada chamada é independente e sem estado. Com objetos distribuídos, o objeto mantém estado entre as chamadas — comprar 100 PETR4 e depois consultar a carteira retorna os 100 PETR4 comprados anteriormente.

**Funcionalidades do objeto Bolsa**
- `cadastrar_ativo(codigo, nome, preco)` — cadastra um novo ativo na bolsa
- `atualizar_preco(codigo, preco)` — atualiza o preço e calcula a variação
- `consultar_ativo(codigo)` — retorna preço atual e variação percentual
- `listar_ativos()` — lista todos os ativos com preços e variações
- `comprar(codigo, quantidade)` — registra uma compra na carteira
- `vender(codigo, quantidade)` — registra uma venda com validação de saldo
- `carteira()` — exibe posição atual e total investido
- `historico()` — exibe todas as operações realizadas

**Tecnologias utilizadas**
- `Pyro5` — biblioteca de objetos distribuídos para Python
- `@Pyro5.api.expose` — decorador para expor métodos remotamente
- `pyro5-ns` — Name Server para descoberta de objetos
- `Vagrant + VirtualBox` — provisionamento das VMs Linux

---

## Arquitetura

```
┌──────────────────┐      descobre objeto      ┌──────────────────────────────┐
│   CLIENT VM      │ ────────────────────────> │   NAME SERVER VM             │
│   192.168.56.12  │   PYRONAME:bolsa          │   192.168.56.10              │
│                  │ <──────────────────────── │   pyro5-ns                   │
│   client.py      │   retorna URI do objeto   └──────────────────────────────┘
│                  │                                        ▲
│                  │        Pyro5 direto                    │ registra
│                  │ ────────────────────────────────────>  │
└──────────────────┘                           ┌──────────────────────────────┐
                                               │   SERVER VM                  │
                                               │   192.168.56.11              │
                                               │   server.py                  │
                                               │   Objeto Bolsa               │
                                               │   ├── cadastrar_ativo        │
                                               │   ├── atualizar_preco        │
                                               │   ├── consultar_ativo        │
                                               │   ├── listar_ativos          │
                                               │   ├── comprar                │
                                               │   ├── vender                 │
                                               │   ├── carteira               │
                                               │   └── historico              │
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
sd-05-objetos-distribuidos/
├── Vagrantfile
├── README.md
├── .gitignore
├── setup/
│   ├── setup-nameserver.sh
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
git clone https://github.com/GustavoRodrigues476/sd-05-objetos-distribuidos
cd sd-05-objetos-distribuidos
```

### 2. Suba as VMs

```bash
vagrant up
```

> Na primeira execução o Vagrant baixa a imagem do Ubuntu (~500MB) e instala o `Pyro5` automaticamente. Aguarde as três VMs aparecerem como `ready`.

Se alguma VM não subir, suba individualmente:

```bash
vagrant up nameserver
vagrant up server
vagrant up client
```

### 3. Abra três terminais

**Terminal 1 — inicie o Name Server:**

```bash
vagrant ssh nameserver
pyro5-ns -n 192.168.56.10
```

**Terminal 2 — inicie o servidor:**

```bash
vagrant ssh server
python3 /vagrant/src/server.py
```

**Terminal 3 — execute o client:**

```bash
vagrant ssh client
python3 /vagrant/src/client.py
```

> **Importante:** sempre inicie o Name Server antes do server e do client.

---

## Saída esperada

**Terminal do Name Server:**
```
Pyro5 Name Server started.
URI = PYRO:Pyro.NameServer@192.168.56.10:9090
```

**Terminal do server:**
```
[Servidor] Objeto Bolsa registrado no Name Server
[Servidor] URI: PYRO:bolsa@192.168.56.11:XXXXX
[Bolsa] COMPRA: 100x PETR4 a R$41.20 = R$4120.00
[Bolsa] COMPRA: 50x VALE3 a R$65.50 = R$3275.00
[Bolsa] COMPRA: 200x ITUB4 a R$32.10 = R$6420.00
[Bolsa] VENDA: 30x PETR4 a R$41.20 = R$1236.00
```

**Terminal do client:**
```
==================================================
 ATIVOS DISPONÍVEIS
==================================================
  PETR4  Petrobras            R$38.50  ▲ +0.00%
  VALE3  Vale                 R$68.20  ▲ +0.00%
  ITUB4  Itaú Unibanco        R$32.10  ▲ +0.00%
  BBDC4  Bradesco             R$14.80  ▲ +0.00%
  MGLU3  Magazine Luiza       R$9.30   ▲ +0.00%

==================================================
 ATUALIZANDO PREÇOS
==================================================
  PETR4 atualizado para R$41.20 (+7.01%)
  VALE3 atualizado para R$65.50 (-3.96%)
  MGLU3 atualizado para R$7.90 (-15.05%)

==================================================
 CARTEIRA ATUAL
==================================================
  PETR4  Petrobras            70x  R$41.20 = R$2884.00
  VALE3  Vale                 50x  R$65.50 = R$3275.00
  ITUB4  Itaú Unibanco        200x R$32.10 = R$6420.00

  Total investido: R$12579.00
```

---

## Solução de problemas

### Erro: `Failed to locate the name server`

O Name Server precisa estar rodando antes do server e do client. Verifique se o terminal 1 está com o `pyro5-ns` ativo.

### Erro: `ModuleNotFoundError: No module named 'Pyro5'`

Execute manualmente dentro da VM:

```bash
vagrant ssh nameserver
pip3 install pyro5

vagrant ssh server
pip3 install pyro5

vagrant ssh client
pip3 install pyro5
```

Ou force o provisionamento novamente:

```bash
vagrant reload --provision
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

### Erro: `VM not created. Moving on...`

Suba a VM individualmente:

```bash
vagrant up nameserver
vagrant up server
vagrant up client
```

---

## Comandos úteis do Vagrant

```bash
vagrant up              # sobe as três VMs
vagrant up nameserver   # sobe só o name server
vagrant up server       # sobe só o server
vagrant up client       # sobe só o client
vagrant ssh nameserver  # acessa o name server via SSH
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
