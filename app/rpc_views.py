from jsonrpc import jsonrpc_method
from app.models import TailSession


@jsonrpc_method('create_session() -> str')
def create_session(request):
    """Create tail session"""
    session = TailSession.objects.create()
    return {
        'hash': session.hash,
        'secret': session.secret,
    }


@jsonrpc_method('add_lines(hash=str, lines=list) -> bool')
def add_lines(request, hash, lines):
    """Add lines to tail session"""
    try:
        session = TailSession.objects.get(hash=hash)
        for line in lines:
            session.add(line.replace('>', '&gt;').replace('<', '&lt;') + u"\n")
        return True
    except TailSession.DoesNotExist:
        return False
