import socket
import json
import sys

SERVER_IP = "192.168.56.10"
PORT = 5001

MODOS = ["simples", "lock", "semaforo1", "semaforo2"]

def executar(modo):
    dados = {"modo": modo, "ri": 3, "c": 1}

    print(f"\n{'='*55}")
    print(f" MODO: {modo.upper()}")
    print(f"{'='*55}")
    print(f"[Client] Enviando para o servidor: {dados}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(json.dumps(dados).encode())
        resposta = json.loads(s.recv(65536).decode())

    print(f"[Client] Resultado recebido ({len(resposta['resultado'])} linhas):")
    for linha in resposta["resultado"]:
        print(f"  {linha}")

def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else None

    if modo and modo in MODOS:
        executar(modo)
    else:
        print("Executando todos os modos...\n")
        for m in MODOS:
            executar(m)
            print()

if __name__ == "__main__":
    main()