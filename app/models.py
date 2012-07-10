from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from hashlib import sha1
from itertools import imap
from assync.client import sender
import os.path
import codecs


class TailSession(models.Model):
    """Tail session"""
    title = models.CharField(max_length=300, verbose_name=_('title'))
    hash = models.CharField(max_length=8, unique=True, verbose_name=_('hash'))

    def save(self, *args, **kwargs):
        """Save with hash generation"""
        if not self.id:
            key = str(TailSession.objects.count())
            while not self.hash or TailSession.objects.filter(hash=self.hash).count():
                key += '1'
                self.hash = sha1(key).hexdigest()[:8]
            if not self.title:
                self.title = 'Tail session %s' % self.hash
            with open(self.log_file_path, 'w'):
                pass
        super(TailSession, self).save(*args, **kwargs)

    def add(self, line):
        """Add line to session"""
        with codecs.open(self.log_file_path, 'a', 'utf-8') as log_file:
            log_file.write(line)
        sender.send(self.hash, line.encode('utf-8'))

    @property
    def log_file_path(self):
        return os.path.join(
            getattr(settings, 'STORE_PATH'),
            self.hash,
        )

    @property
    def log_file_url(self):
        return os.path.join(
            getattr(settings, 'STORE_URL'),
            self.hash,
        )

    @property
    def content(self):
        with open(self.log_file_path) as log_file:
            return log_file.read()
