import time

from src.utils.parallel import parallelise
from src.utils.tracer import trace_function

trace_sleep = trace_function(time.sleep)
parallelise_sleep = parallelise(trace_sleep)


@trace_function
def multi_sleep(num, delay):
    for _ in range(num):
        parallelise_sleep(delay)
