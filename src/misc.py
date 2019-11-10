import time
from argparse import ArgumentParser

from src.util.parallel import parallelise
from src.util.tracer import trace_function


@parallelise
@trace_function
def sleep(delay=1.0):
    print("sleep, {} seconds".format(delay))
    time.sleep(delay)
    print("sleep done".format(delay))


@trace_function
def multi_sleep(num=3, delay=1.0):
    for _ in range(num):
        sleep(delay)


if __name__ == "__main__":
    parser = ArgumentParser()
    args = parser.parse_args()
    parser.add_argument("--num", type=int, default=3)
    parser.add_argument("--delay", type=float, default=1.0)

    multi_sleep(args.num, args.delay)
