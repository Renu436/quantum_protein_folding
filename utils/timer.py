import time

def measure(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, round(end-start, 4)