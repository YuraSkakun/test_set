def add(a, b):
    return a + b


class frange:
    def __init__(self, *args):
        self._data = range(*args)

    def __iter__(self):
        return iter(self._data)


assert list(frange(5)) == [0, 1, 2, 3, 4]
assert list(frange(1, 5)) == [1, 2, 3, 4]

print('SUCCESS!')
