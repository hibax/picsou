from threading import Timer


def repeat_timer(interval, fct, args=None, kwargs=None):
    fct(*args, **kwargs)
    Timer(interval, repeat_timer, (interval, fct, args, kwargs)).start()


def create_repeated_timer(fct, interval, *args, **kwargs):
    return Timer(interval, repeat_timer, (interval, fct, args, kwargs))
