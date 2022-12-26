import multiprocessing
import time
from random import random


class MeasureAndPrint:
    def __init__(self, async_=False):
        self.async_ = async_

    def __call__(self, func):
        def _measure_and_print(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start} seconds")
            return result

        async def _measure_and_print_async(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start} seconds")
            return result

        return _measure_and_print_async if self.async_ else _measure_and_print


class Euler(multiprocessing.Process):
    def __init__(self,q,num_samples):
        super().__init__()
        self.q = q
        self.i = 0
        self.num_samples = num_samples
        self.d = dict()

    def run(self):
        def return_i():
            accum = random()
            for i in range(2, 100000):
                accum += random()
                if accum > 1.0:
                    self.i = i
                    return self.i

        for _ in range(self.num_samples):
            count = return_i()
            if count not in self.d:
                self.d[count] = 0
            self.d[count] += 1

        self.q.put(self.d)


@MeasureAndPrint()
def e(m,n):
    q = multiprocessing.Queue()
    processes = [Euler(q,n) for _ in range(m)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    for samps, count_of_samps in sorted(q.get().items()):
        print(f"{samps}:{count_of_samps}")

    print(f"Euler's Number : {sum([k * v for k, v in q.get().items()]) / n}")


if __name__ == "__main__":
    print(e(multiprocessing.cpu_count(),1000000))


