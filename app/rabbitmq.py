import pika
import json

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="user_registration")

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"Message reçu : {message}")

    channel.basic_consume(queue="user_registration", on_message_callback=callback, auto_ack=True)

    print("Espera de mensajes...")
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages()
