from time import time


def call_measuring_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        print(f'Starting {func.__name__}')
        func(*args, **kwargs)
        end = time()
        print(f'{func.__name__} took {end - start} seconds')

    return wrapper
