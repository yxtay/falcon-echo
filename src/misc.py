import time

from src.util.parallel import parallelise
from src.util.tracer import trace_function

trace_sleep = trace_function(time.sleep)
parallelise_sleep = parallelise(trace_sleep)


@trace_function
def multi_sleep(num, delay):
    for _ in range(num):
        parallelise_sleep(delay)
