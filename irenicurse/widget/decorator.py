def bind_to_key(key):
    """
    A decorator to bind the call of a widget's method to a key press event.

    It will not change the method signature.
    """
    def decorate(func):
        func.__keys__ = func.__keys__ + [key] if hasattr(func, "__keys__") else [key]
        return func
    return decorate
