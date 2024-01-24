"""
trying a little bit of decorators
"""

import time
import functools
import timeit


TIMERS = dict()

def register_timer(func):
  """
  Register a timer decorator
  
  TIMERS and the register_timer-function can be considered a "light-weight plugin architectur" 
  """
  TIMERS[func.__name__] = func
  return func

@register_timer
def timer(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    duration = end - start
    print(f"{func.__name__} toke {duration:.4f} secs")
  return wrapper

@register_timer
def timer_timeit(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start = timeit.timeit()
    func(*args, **kwargs)
    end = timeit.timeit()
    duration = end - start
    print(f"{func.__name__} toke {duration:.4f} secs")
  return wrapper

def debug(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    value = func(*args, **kwargs)
    args_repr = [repr(arg) for arg in args]
    kwargs_repr = [f"{key}={repr(value)}" for key, value in kwargs.items()]
    print(f"return value of {func.__name__!r} is {value}")
    print(f"positional args: {args_repr}")
    print(f"keyword args: {kwargs_repr}")
    return value
  return wrapper

def sleeper(_func=None, *, sec=1):
  """can be called with and without (keyword-)arguments"""
  def inner_sleeper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      time.sleep(sec)
      value = func(*args, **kwargs)
      return value
    return wrapper
  
  if _func == None:
    return inner_sleeper         # @sleeper(sec=4)
  else:
    return inner_sleeper(_func)  # @sleeper

def sleeper_with_args(sec):
  def inner_sleeper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      time.sleep(sec)
      return func(*args, **kwargs)
    return wrapper
  return inner_sleeper

def counter(func):
  """stateful decorator"""
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    wrapper.count += 1
    print(f"{func.__name__} was called {wrapper.count} time(s).")
    return func(*args, **kwargs)
  wrapper.count = 0
  return wrapper

class Counter:
  """another way of saving the state -> stateful decorator"""
  def __init__(self, func) -> None:
    """takes the decorated function as the argument"""
    functools.update_wrapper(self, func)  # instead of @functools.wraps(func)
    self.func = func
    self.count = 0
  
  def __call__(self, *args, **kwargs):    # this is basically the wrapper(*args, **kwargs)
    """
    if this is implemented, the class is callable
    
    everytime an instance of the class is called, the __call__() method is executed
    counter = Counter()
    counter()  # first time
    counter()  # second time
    ...
    """
    self.count += 1
    print(f"{self.func.__name__} was called {self.count} time(s).")
    return self.func(*args, **kwargs)




"""TIMERS and Sleeper-class are both options to capsulate functionality in one file"""
class Sleeper:
  @staticmethod
  def sleeper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      time.sleep(1)
      value = func(*args, **kwargs)
      return value
    return wrapper

class Circle:
  def __init__(self, radius) -> None:
    self.radius = radius
  
  @classmethod
  def unit_circle(cls):
    return cls(1)

if __name__ == "__main__":
  c = Circle.unit_circle()
  print(c)
  c2 = Circle(2)
  print(c2)
  print(type(c))
  print(c.radius)