import time

current_time = time.time()
print(current_time)
def decorator_time(function):
    def wrapper_functions():
        function()
        new_time = time.time() - current_time
    return wrapper_functions

@decorator_time
def speed_calc_decorator():
    pass

@decorator_time
def fast_function():
    for i in range(1000000):
        i * i

@decorator_time
def slow_function():
    for i in range(10000000):
        i * i