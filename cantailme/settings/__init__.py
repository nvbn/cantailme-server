try:
    from base import *
    from local import *
except ImportError:
    raise Exception('Copy dist.py to local.py and fill settings')
