import socket
import threading

HOST = ''
PORT = 5000

def handle_client(con, cliente):
    print(f"[Servidor] Client conectado: {cliente}")
    try:
        msg = con.recv(1024)
        N = msg.decode().split(";")

        x = float(N[0])
        y = float(N[1])
        op = N[2].strip()

        if op == "soma":
            z = x + y
        elif op == "subtracao":
            z = x - y
        elif op == "multiplicacao":
            z = x * y
        elif op == "divisao":
            if y == 0:
                con.send("Erro: divisao por zero".encode())
                return
            z = x / y
        elif op == "potencia":
            z = x ** y
        elif op == "modulo":
            z = x % y
        else:
            con.send("Erro: operacao invalida".encode())
            return

        resultado = f"{x} {op} {y} = {z}"
        print(f"[Servidor] {resultado} | client: {cliente}")
        con.send(str(z).encode())

    except Exception as e:
        print(f"[Servidor] Erro com client {cliente}: {e}")
        con.send("Erro: verifique os dados enviados".encode())
    finally:
        con.close()
        print(f"[Servidor] Conexão encerrada: {cliente}")

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(5)
    print(f"[Servidor] Aguardando conexões na porta {PORT}...")
    print(f"[Servidor] Operações disponíveis: soma, subtracao, multiplicacao, divisao, potencia, modulo")

    while True:
        con, cliente = tcp.accept()
        t = threading.Thread(target=handle_client, args=(con, cliente))
        t.start()
        print(f"[Servidor] Threads ativas: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()