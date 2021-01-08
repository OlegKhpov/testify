def frange(start, stop=None, step=None):
    if step is None:
        step = 0.5
    if stop is None:
        stop = float(start)
        start = 0
    while True:
        if start >= stop:
            break
        yield start
        start += step


# if __name__ == "__main__":
#     for i in frange(1, 100, 3.5):
#         print(i)
#     print('Completed first')


class Frange:
    def __init__(self, start, stop=None, step=None):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.step is None:
            self.step = 0.5
        if self.stop is None:
            self.stop = float(self.start)
            self.start = 0
        if self.start >= self.stop:
            raise StopIteration
        number = self.start
        self.start += self.step
        return number


# if __name__ == "__main__":
#     fr = Frange(1, 100, 3.5)
#     print(next(fr))
#     print(next(fr))
#     print(next(fr))
#     print(next(fr))
#     print(next(fr))
#     print('Complete second')

#     fr = Frange(1, 100, 3.5)
#     it = iter(fr)
#     print(next(it))
#     print(next(it))
#     print(next(it))
#     print(next(it))
#     print(next(it))
#     print('complete third')

#     for i in Frange(1, 100, 3.5):
#         print(i)
#     print('Complete fourth')
