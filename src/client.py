import socket
import sys

HOST = '192.168.56.10'
PORT = 5000

OPERACOES = ["soma", "subtracao", "multiplicacao", "divisao", "potencia", "modulo"]

def calcular(x, y, operacao):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    msg = f"{x};{y};{operacao}"
    print(f"[Client] Enviando: {msg}")
    tcp.send(msg.encode())

    resposta = tcp.recv(1024)
    resultado = resposta.decode()
    print(f"[Client] Resultado: {resultado}")
    tcp.close()
    return resultado

def main():
    print("=== Calculadora Distribuída ===")
    print(f"Operações disponíveis: {', '.join(OPERACOES)}\n")

    operacoes_teste = [
        (10, 5, "soma"),
        (10, 5, "subtracao"),
        (10, 5, "multiplicacao"),
        (10, 5, "divisao"),
        (2,  8, "potencia"),
        (10, 3, "modulo"),
    ]

    for x, y, op in operacoes_teste:
        print(f"\n--- {op.upper()} ---")
        calcular(x, y, op)

if __name__ == "__main__":
    main()