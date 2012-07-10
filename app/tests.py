from django.test import TestCase
from app.models import TailSession


class TailTest(TestCase):
    def test_add(self):
        session = TailSession.objects.create()
        res = ''
        for i in range(1000):
            session.add(str(i))
            res += str(i) + '\n'
        self.assertEqual(
            session.content, res,
            'Add lines to tail session',
        )
