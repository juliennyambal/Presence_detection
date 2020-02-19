from kombu import Connection, Exchange, Producer, Queue, Consumerconn = Connection("amqp://localhost:5672")
exchange = Exchange("rpc", type="direct")request_queue = Queue(name="rpc", exchange=exchange, routing_key="request")
request_queue.maybe_bind(conn)
request_queue.declare()def process_message(body, message):
    print("Request: %s" % body)
    message.ack()    # send reply to client
    producer = Producer(channel=conn, routing_key=message.properties['reply_to'])
    producer.publish("result")with Consumer(conn, request_queue, callbacks=[process_message]):
    conn.drain_events()