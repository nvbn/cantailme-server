from django.core.management.base import BaseCommand
from django.conf import settings
from sockjs.tornado import SockJSRouter
from assync.server import PushConnection, RBClient
import tornado.web
import tornado.ioloop
import tornado.gen


class Command(BaseCommand):
    help = 'Run push server'

    def handle(self, *args, **kwargs):
        EchoRouter = SockJSRouter(PushConnection, '/assync', {
            'sockjs_url': 'http://cdn.sockjs.org/sockjs-0.3.min.js',
        })
        application = tornado.web.Application(
            EchoRouter.urls,
            port=settings.TORNADO_PORT,
            debug=settings.DEBUG,
        )
        pc = RBClient(
            application,
            settings.PIKA_HOST,
            settings.PIKA_QUEUE,
            'cantailme.*',
        )
        application.listen(settings.TORNADO_PORT)
        PushConnection.rb = pc
        ioloop = tornado.ioloop.IOLoop.instance()
        pc.connect()
        ioloop.start()
