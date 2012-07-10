from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
from app.models import TailSession


@render_to('app/index.html')
def index(request):
    """Index page"""
    return {}


@render_to('app/tail.html')
def tail(request, hash):
    """Display by hash"""
    return {
        'session': get_object_or_404(TailSession, hash=hash),
    }
