import pika
import json
import uuid
from datetime import datetime

BROKER_IP = "192.168.56.10"

credenciais = pika.PlainCredentials('meuapp', 'senha123')
parametros = pika.ConnectionParameters(
    host=BROKER_IP,
    port=5672,
    virtual_host='/',
    credentials=credenciais,
    heartbeat=60
)

pedidos = [
    {"produto": "Notebook Dell",    "quantidade": 1, "valor": 3500.00},
    {"produto": "Mouse Logitech",   "quantidade": 2, "valor":   89.90},
    {"produto": "Teclado Mecânico", "quantidade": 1, "valor":  299.90},
    {"produto": "Monitor LG 24\"",  "quantidade": 1, "valor": 1200.00},
    {"produto": "Headset Sony",     "quantidade": 1, "valor":  450.00},
]

def main():
    conexao = pika.BlockingConnection(parametros)
    canal = conexao.channel()

    canal.queue_declare(queue='pedidos', durable=True)

    print(f"[Produtor] Conectado ao broker {BROKER_IP}")
    print(f"[Produtor] Enviando {len(pedidos)} pedidos...\n")

    for item in pedidos:
        pedido = {
            "id":         str(uuid.uuid4())[:8].upper(),
            "produto":    item["produto"],
            "quantidade": item["quantidade"],
            "valor":      item["valor"],
            "total":      item["quantidade"] * item["valor"],
            "hora":       datetime.now().strftime("%H:%M:%S")
        }

        canal.basic_publish(
            exchange='',
            routing_key='pedidos',
            body=json.dumps(pedido),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        print(f"[Produtor] Pedido enviado: #{pedido['id']} | {pedido['produto']} | R${pedido['total']:.2f}")

    conexao.close()
    print(f"\n[Produtor] Todos os pedidos enviados ao broker.")

if __name__ == "__main__":
    main()