from time import perf_counter


def measure_time(func):
    """Decorator to measure the execution time of functions."""

    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took: {perf_counter() - start:.2f} seconds")
        return result

    return wrapper