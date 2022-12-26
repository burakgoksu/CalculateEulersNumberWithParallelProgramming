import math
import multiprocessing
import time


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
    def __init__(self,n,q,s,f):
        super().__init__()
        self.n = n
        self.q = q
        self.sum = 0
        self.s = s
        self.f = f

    def run(self):
        for i in range(self.s,self.f):
            self.sum += 1/math.factorial(i)
        self.q.put(self.sum)


@MeasureAndPrint()
def estimate(m,n):
    h = n//m
    q = multiprocessing.Queue()
    processes = []
    start = 0
    finish = n

    for i in range(m):
        p = Euler(n,q,start,start+h)
        start += h
        processes.append(p)
        if start >= finish:
            break

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return sum(q.get() for _ in processes)

if __name__ == "__main__":
    print(f"Euler's Number: {estimate(multiprocessing.cpu_count(),10000)}")