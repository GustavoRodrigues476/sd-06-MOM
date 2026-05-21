import socket
import threading
import json
import time

HOST = "0.0.0.0"
PORT = 5001

lock = threading.Lock()
semaforo1 = threading.Semaphore(1)
semaforo2 = threading.Semaphore(2)

resultados = []
resultados_lock = threading.Lock()

def fun_simples(ri, c, thread_id):
    ni = 100 * c
    nj = 100 * c
    n = 0
    for i in range(ni):
        for j in range(nj):
            n = n + 1
    for i in range(ri):
        time.sleep(0.1)
        msg = f"[Thread {thread_id}] (sem sincronização) n={n} | i={i}"
        print(msg)
        with resultados_lock:
            resultados.append(msg)

def fun_lock(ri, c, thread_id):
    ni = 100 * c
    nj = 100 * c
    n = 0
    for i in range(ni):
        for j in range(nj):
            n = n + 1
    print(f"[Thread {thread_id}] Aguardando Lock...")
    lock.acquire()
    print(f"[Thread {thread_id}] Lock ADQUIRIDO")
    for i in range(ri):
        time.sleep(0.1)
        msg = f"[Thread {thread_id}] (lock) n={n} | i={i}"
        print(msg)
        with resultados_lock:
            resultados.append(msg)
    lock.release()
    print(f"[Thread {thread_id}] Lock LIBERADO")

def fun_semaforo1(ri, c, thread_id):
    ni = 100 * c
    nj = 100 * c
    n = 0
    for i in range(ni):
        for j in range(nj):
            n = n + 1
    print(f"[Thread {thread_id}] Aguardando Semáforo(1)...")
    semaforo1.acquire()
    print(f"[Thread {thread_id}] Semáforo(1) ADQUIRIDO")
    for i in range(ri):
        time.sleep(0.1)
        msg = f"[Thread {thread_id}] (semaforo1) n={n} | i={i}"
        print(msg)
        with resultados_lock:
            resultados.append(msg)
    semaforo1.release()
    print(f"[Thread {thread_id}] Semáforo(1) LIBERADO")

def fun_semaforo2(ri, c, thread_id):
    ni = 100 * c
    nj = 100 * c
    n = 0
    for i in range(ni):
        for j in range(nj):
            n = n + 1
    print(f"[Thread {thread_id}] Aguardando Semáforo(2)...")
    semaforo2.acquire()
    print(f"[Thread {thread_id}] Semáforo(2) ADQUIRIDO")
    for i in range(ri):
        time.sleep(0.1)
        msg = f"[Thread {thread_id}] (semaforo2) n={n} | i={i}"
        print(msg)
        with resultados_lock:
            resultados.append(msg)
    semaforo2.release()
    print(f"[Thread {thread_id}] Semáforo(2) LIBERADO")

def executar_modo(modo, ri, c):
    global resultados
    resultados = []

    modos = {
        "simples":   fun_simples,
        "lock":      fun_lock,
        "semaforo1": fun_semaforo1,
        "semaforo2": fun_semaforo2,
    }

    fn = modos.get(modo)
    if not fn:
        return ["Modo inválido. Use: simples, lock, semaforo1, semaforo2"]

    print(f"\n[Servidor] Iniciando modo: {modo.upper()}")
    threads = []
    for i in range(1, 5):
        t = threading.Thread(target=fn, args=(ri, i, i))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return resultados

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[Servidor] Aguardando conexões em {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[Servidor] Client conectado: {addr}")
                dados = json.loads(conn.recv(1024).decode())
                modo = dados.get("modo", "simples")
                ri   = dados.get("ri", 3)
                c    = dados.get("c", 1)

                resultado = executar_modo(modo, ri, c)
                conn.sendall(json.dumps({"modo": modo, "resultado": resultado}).encode())

if __name__ == "__main__":
    main()