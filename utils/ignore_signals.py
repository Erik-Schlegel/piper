import signal

def ignore_signals():
    """
    Play calls are handled in a separate process. Ignore signal handlers
    internally, oherwise we get errors on exit.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)