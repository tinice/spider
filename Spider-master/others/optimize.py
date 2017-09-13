import math
from functools import wraps
from time import time


def count_time(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time()
        r = func(*args,**kwargs)
        end = time()
        print('{}.{}: {}'.format(func.__module__,func.__name__,end-start))
        return r
    return wrapper


def compute_roots(nums):
    result = []
    sqrt = math.sqrt
    result_append = result.append
    for n in nums:
        result_append(sqrt(n))
    return result

@count_time
def test():
    nums = range(100000)
    for n in range(200):
        r = compute_roots(nums)

if __name__ == '__main__':
    test()
