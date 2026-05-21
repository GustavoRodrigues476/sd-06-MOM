import socket
import Pyro5.api
import Pyro5.server
from datetime import datetime

@Pyro5.api.expose
class Bolsa(object):

    def __init__(self):
        self._ativos = {
            "PETR4": {"nome": "Petrobras",        "preco": 38.50, "preco_anterior": 38.50},
            "VALE3": {"nome": "Vale",              "preco": 68.20, "preco_anterior": 68.20},
            "ITUB4": {"nome": "Itaú Unibanco",    "preco": 32.10, "preco_anterior": 32.10},
            "BBDC4": {"nome": "Bradesco",          "preco": 14.80, "preco_anterior": 14.80},
            "MGLU3": {"nome": "Magazine Luiza",   "preco": 9.30,  "preco_anterior": 9.30},
        }
        self._carteira = {}   # {codigo: quantidade}
        self._historico = []  # lista de operações

    def cadastrar_ativo(self, codigo, nome, preco):
        self._ativos[codigo] = {
            "nome": nome,
            "preco": float(preco),
            "preco_anterior": float(preco)
        }
        print(f"[Bolsa] Ativo cadastrado: {codigo} - {nome} R${preco}")
        return f"Ativo {codigo} cadastrado com sucesso."

    def atualizar_preco(self, codigo, novo_preco):
        if codigo not in self._ativos:
            raise ValueError(f"Ativo {codigo} não encontrado.")
        self._ativos[codigo]["preco_anterior"] = self._ativos[codigo]["preco"]
        self._ativos[codigo]["preco"] = float(novo_preco)
        variacao = self._calcular_variacao(codigo)
        print(f"[Bolsa] Preço atualizado: {codigo} R${novo_preco} ({variacao:+.2f}%)")
        return f"{codigo} atualizado para R${novo_preco:.2f} ({variacao:+.2f}%)"

    def consultar_ativo(self, codigo):
        if codigo not in self._ativos:
            raise ValueError(f"Ativo {codigo} não encontrado.")
        ativo = self._ativos[codigo]
        variacao = self._calcular_variacao(codigo)
        return {
            "codigo": codigo,
            "nome": ativo["nome"],
            "preco": ativo["preco"],
            "preco_anterior": ativo["preco_anterior"],
            "variacao": round(variacao, 2)
        }

    def listar_ativos(self):
        resultado = []
        for codigo, ativo in self._ativos.items():
            variacao = self._calcular_variacao(codigo)
            resultado.append({
                "codigo": codigo,
                "nome": ativo["nome"],
                "preco": ativo["preco"],
                "variacao": round(variacao, 2)
            })
        return resultado

    def comprar(self, codigo, quantidade):
        if codigo not in self._ativos:
            raise ValueError(f"Ativo {codigo} não encontrado.")
        quantidade = int(quantidade)
        preco = self._ativos[codigo]["preco"]
        total = preco * quantidade
        self._carteira[codigo] = self._carteira.get(codigo, 0) + quantidade
        operacao = {
            "tipo": "COMPRA",
            "codigo": codigo,
            "quantidade": quantidade,
            "preco": preco,
            "total": round(total, 2),
            "hora": datetime.now().strftime("%H:%M:%S")
        }
        self._historico.append(operacao)
        print(f"[Bolsa] COMPRA: {quantidade}x {codigo} a R${preco:.2f} = R${total:.2f}")
        return operacao

    def vender(self, codigo, quantidade):
        if codigo not in self._ativos:
            raise ValueError(f"Ativo {codigo} não encontrado.")
        quantidade = int(quantidade)
        disponivel = self._carteira.get(codigo, 0)
        if quantidade > disponivel:
            raise ValueError(f"Quantidade insuficiente. Você tem {disponivel} {codigo}.")
        preco = self._ativos[codigo]["preco"]
        total = preco * quantidade
        self._carteira[codigo] -= quantidade
        operacao = {
            "tipo": "VENDA",
            "codigo": codigo,
            "quantidade": quantidade,
            "preco": preco,
            "total": round(total, 2),
            "hora": datetime.now().strftime("%H:%M:%S")
        }
        self._historico.append(operacao)
        print(f"[Bolsa] VENDA: {quantidade}x {codigo} a R${preco:.2f} = R${total:.2f}")
        return operacao

    def carteira(self):
        resultado = []
        total_investido = 0
        for codigo, quantidade in self._carteira.items():
            if quantidade > 0:
                preco = self._ativos[codigo]["preco"]
                total = preco * quantidade
                total_investido += total
                resultado.append({
                    "codigo": codigo,
                    "nome": self._ativos[codigo]["nome"],
                    "quantidade": quantidade,
                    "preco_atual": preco,
                    "total": round(total, 2)
                })
        return {"posicoes": resultado, "total_investido": round(total_investido, 2)}

    def historico(self):
        return list(self._historico)

    def _calcular_variacao(self, codigo):
        ativo = self._ativos[codigo]
        anterior = ativo["preco_anterior"]
        if anterior == 0:
            return 0.0
        return ((ativo["preco"] - anterior) / anterior) * 100


def main():
    ns = Pyro5.api.locate_ns(host="192.168.56.10")
    ns_host = ns._pyroUri.host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ns_host, 80))
    host_local = s.getsockname()[0]
    s.close()

    daemon = Pyro5.server.Daemon(host=host_local)
    bolsa = Bolsa()
    uri = daemon.register(bolsa, objectId="bolsa")
    ns.register("bolsa", uri)
    print(f"[Servidor] Objeto Bolsa registrado no Name Server")
    print(f"[Servidor] URI: {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()