import pika
import json
import time

BROKER_IP = "192.168.56.10"

credenciais = pika.PlainCredentials('meuapp', 'senha123')
parametros = pika.ConnectionParameters(
    host=BROKER_IP,
    port=5672,
    virtual_host='/',
    credentials=credenciais,
    heartbeat=60,
    blocked_connection_timeout=300
)

def processar_pedido(ch, method, properties, body):
    pedido = json.loads(body.decode('utf-8'))

    print(f"\n[Consumidor] Pedido recebido:")
    print(f"  ID:       #{pedido['id']}")
    print(f"  Produto:  {pedido['produto']}")
    print(f"  Qtd:      {pedido['quantidade']}")
    print(f"  Valor:    R${pedido['valor']:.2f}")
    print(f"  Total:    R${pedido['total']:.2f}")
    print(f"  Hora:     {pedido['hora']}")
    print(f"[Consumidor] Processando...")

    time.sleep(2)

    print(f"[Consumidor] Pedido #{pedido['id']} confirmado!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    conexao = pika.BlockingConnection(parametros)
    canal = conexao.channel()

    canal.queue_declare(queue='pedidos', durable=True)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(
        queue='pedidos',
        on_message_callback=processar_pedido
    )

    print(f"[Consumidor] Conectado ao broker {BROKER_IP}")
    print(f"[Consumidor] Aguardando pedidos... (CTRL+C para sair)\n")
    canal.start_consuming()

if __name__ == "__main__":
    main()