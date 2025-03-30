class LockPicker_gkunchev:
    """Pick a lock."""

    def __init__(self, lock):
        self._lock = lock

    def unlock(self):
        combination = []
        while True:
            try:
                self._lock.pick(*combination)
            except TypeError as ex:
                if ex.position is None:
                    combination = [None for _ in range(ex.expected)]
                else:
                    combination[ex.position - 1] = ex.expected()
            except ValueError as ex:
                combination[ex.position - 1] = ex.expected
            else:
                break