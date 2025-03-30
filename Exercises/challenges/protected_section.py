class ProtectedSection:
    """A context manager that allows us to execute a relatively error-free block of code."""
    def __init__(self, log=(), suppress=()):
        self.log = log
        self.suppress = suppress
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            if exc_type in self.log:
                self.exception = exc_value
                return True
            elif exc_type in self.suppress:
                return True
        return False
