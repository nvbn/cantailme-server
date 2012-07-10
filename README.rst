Server side of CanTail.Me
=========================

Deployment
----------
#. Install dependens with ``pip install -r requirements.txt``
#. In ``cantailme/settings/`` copy ``dist.py`` to ``local.py`` and fill it.
#. Init db with ``./manage.py syncdb``
#. Run django server with ``./manage.py runserver``
#. And tornado with ``./manage.py runpush``


For more information visit `cantail.me <http://cantail.me/>`_
