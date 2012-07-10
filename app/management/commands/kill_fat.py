from django.core.management.base import BaseCommand
from django.conf import settings
import commands
import os


class Command(BaseCommand):
    help = 'Kill fat files'

    def handle(self, *args, **kwargs):
        files = commands.getoutput('find %s -size 2M' % 
            getattr(settings, 'STORE_PATH'),
        )
        for fat_file in files.split('\n'):
            if len(fat_file):
                os.system('echo> %s' % fat_file)
