from kombu import Connection, Exchange, Producer, Queue, Consumerconn = Connection("amqp://localhost:5672")
exchange = Exchange("rpc", type="direct")def process_message(body, message):
    print("Response: %s" % body)
    message.ack()reply_queue = Queue(name="amq.rabbitmq.reply-to")
with Consumer(conn, reply_queue, callbacks=[process_message], no_ack=True):
    producer = Producer(exchange=exchange, channel=conn, routing_key="request")
    properties = {
        "reply_to": "amq.rabbitmq.reply-to",
    }    producer.publish("Hello World", **properties)
    conn.drain_events()