from stormed import Connection
from tornado.netutil import TCPServer
from sockjs.tornado import SockJSConnection
import tornado.ioloop
import tornado.gen


class RBClient(object):
    def __init__(self, app, host, queue, key):
        self.app = app
        self.queue = queue
        self.host = host
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.key = key
        self.mq = {}

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        self.connection = Connection(
            host=self.host,
        )
        self.connection.connect(self.on_connected)
        self.connection.on_disconnect = self.on_closed

    def on_connected(self):
        self.connected = True
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.queue,
            type='topic',
            durable=False,
        )
        self.channel.queue_declare(
            queue=self.queue,
            auto_delete=True,
            durable=False,
        )
        self.channel.queue_bind(
            exchange=self.queue,
            queue=self.queue,
            routing_key=self.key,
        )
        self.channel.consume(
            self.queue,
            self.callback,
            no_ack=True,
        )

    def on_basic_cancel(self, frame):
        self.connection.close()

    def on_closed(self, connection):
        tornado.ioloop.IOLoop.instance().stop()

    def callback(self, msg):
        subscribers = self.mq.get(msg.rx_data.routing_key, None)
        if subscribers:
            for subscriber in subscribers:
                subscriber.release(msg.body)


class PushConnection(SockJSConnection):
    def on_message(self, hash):
        self.rb.mq['cantailme.%s' % hash] = self.rb.mq.get('cantailme.%s' % hash, []) + [self]

    def release(self, data):
        self.send(data)
