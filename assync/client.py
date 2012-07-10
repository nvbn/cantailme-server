from django.conf import settings
import pika


class PikaSender(object):
    def send(self, hash, line):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            settings.PIKA_HOST))
        self.channel = self.connection.channel()
        self.channel.basic_publish(
            exchange=settings.PIKA_QUEUE,
            routing_key='cantailme.%s' % hash,
            body=line,

        )
        self.connection.close()


sender = PikaSender()
