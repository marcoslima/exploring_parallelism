import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from multiprocessing import Pool

from helpers import call_measuring_time

FIBO_SIZE = 30
FIBOS_TO_GET = 50


def fibo(n):
    if n <= 1:
        return n
    return fibo(n - 1) + fibo(n - 2)


@call_measuring_time
def singlethread():
    result = 0
    for _ in range(FIBOS_TO_GET):
        result += fibo(FIBO_SIZE)
    print(f'Singlethread result: {result}')


@call_measuring_time
def multithread():
    num_workers = min(FIBOS_TO_GET, os.cpu_count())
    print(f'Using {num_workers} workers')
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(fibo, [FIBO_SIZE] * FIBOS_TO_GET)
    result = sum(results)
    print(f'Multithread result: {result}')


@call_measuring_time
def multiproc():
    num_procs = min(FIBOS_TO_GET, os.cpu_count())
    print(f'Using {num_procs} processes')
    with Pool(num_procs) as executor:
        results = executor.map(fibo, [FIBO_SIZE] * FIBOS_TO_GET)
    print(f'Multiprocess result: {sum(results)}')


def main():
    singlethread()
    multithread()
    multiproc()


if __name__ == '__main__':
    main()
