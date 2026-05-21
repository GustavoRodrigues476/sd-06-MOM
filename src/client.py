import Pyro5.api

NS_HOST = "192.168.56.10"

def separador(titulo):
    print(f"\n{'='*50}")
    print(f" {titulo}")
    print(f"{'='*50}")

def main():
    print(f"[Client] Conectando ao Name Server {NS_HOST}...")
    bolsa = Pyro5.api.Proxy(f"PYRONAME:bolsa@{NS_HOST}")

    separador("ATIVOS DISPONÍVEIS")
    for ativo in bolsa.listar_ativos():
        sinal = "▲" if ativo["variacao"] >= 0 else "▼"
        print(f"  {ativo['codigo']:<6} {ativo['nome']:<20} R${ativo['preco']:.2f}  {sinal} {ativo['variacao']:+.2f}%")

    separador("CADASTRANDO NOVO ATIVO")
    print(bolsa.cadastrar_ativo("WEGE3", "WEG", 45.80))

    separador("ATUALIZANDO PREÇOS")
    print(bolsa.atualizar_preco("PETR4", 41.20))
    print(bolsa.atualizar_preco("VALE3", 65.50))
    print(bolsa.atualizar_preco("MGLU3", 7.90))

    separador("CONSULTANDO ATIVO")
    ativo = bolsa.consultar_ativo("PETR4")
    print(f"  Código:         {ativo['codigo']}")
    print(f"  Nome:           {ativo['nome']}")
    print(f"  Preço anterior: R${ativo['preco_anterior']:.2f}")
    print(f"  Preço atual:    R${ativo['preco']:.2f}")
    print(f"  Variação:       {ativo['variacao']:+.2f}%")

    separador("COMPRANDO ATIVOS")
    op = bolsa.comprar("PETR4", 100)
    print(f"  {op['tipo']}: {op['quantidade']}x {op['codigo']} a R${op['preco']:.2f} = R${op['total']:.2f}")
    op = bolsa.comprar("VALE3", 50)
    print(f"  {op['tipo']}: {op['quantidade']}x {op['codigo']} a R${op['preco']:.2f} = R${op['total']:.2f}")
    op = bolsa.comprar("ITUB4", 200)
    print(f"  {op['tipo']}: {op['quantidade']}x {op['codigo']} a R${op['preco']:.2f} = R${op['total']:.2f}")

    separador("VENDENDO ATIVOS")
    op = bolsa.vender("PETR4", 30)
    print(f"  {op['tipo']}: {op['quantidade']}x {op['codigo']} a R${op['preco']:.2f} = R${op['total']:.2f}")

    separador("CARTEIRA ATUAL")
    carteira = bolsa.carteira()
    for pos in carteira["posicoes"]:
        print(f"  {pos['codigo']:<6} {pos['nome']:<20} {pos['quantidade']}x R${pos['preco_atual']:.2f} = R${pos['total']:.2f}")
    print(f"\n  Total investido: R${carteira['total_investido']:.2f}")

    separador("HISTÓRICO DE OPERAÇÕES")
    for op in bolsa.historico():
        print(f"  [{op['hora']}] {op['tipo']:<6} {op['quantidade']}x {op['codigo']} a R${op['preco']:.2f} = R${op['total']:.2f}")

    separador("TESTE DE ERRO")
    try:
        bolsa.vender("PETR4", 9999)
    except Exception as e:
        print(f"  Erro capturado: {e}")

if __name__ == "__main__":
    main()