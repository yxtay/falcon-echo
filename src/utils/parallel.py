import functools
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Process
from threading import Thread


def parallelise(func=None, is_multiprocess=False):
    if func is None:
        return functools.partial(parallelise, is_multiprocess=is_multiprocess)

    PoolExecutor = ProcessPoolExecutor if is_multiprocess else ThreadPoolExecutor

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        executor = PoolExecutor()
        task = executor.submit(func, *args, **kwargs)
        executor.shutdown(wait=False)
        return task

    return wrapped


def multithread(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapped


def multiprocess(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        process = Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process

    return wrapped
