import math
import threading
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


class Euler(threading.Thread):
    def __init__(self,n,i):
        super().__init__()
        self.n = n
        self.i = i
        self.sum = 0

    def run(self):
        for i in range(self.n):
            self.sum += 1/math.factorial(i)

@MeasureAndPrint()
def main():
    num = 10000
    num_threads = 16
    num_per_thread = num//num_threads
    threads = []
    for i in range(num_threads):
        t = Euler(num_per_thread,i)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    num_lists = []
    summ = 0
    for t in threads:
        num_lists.append(t.sum)
        summ += t.sum
    for i in num_lists:
        print(i)

    print("------------------------------")
    print(summ/num_threads)


if __name__ == "__main__":
    print(main())