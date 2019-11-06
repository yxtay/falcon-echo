import functools
import inspect
from contextlib import contextmanager

from opencensus.common.transports.async_ import AsyncTransport
from opencensus.ext.stackdriver.trace_exporter import StackdriverExporter
from opencensus.trace.execution_context import get_opencensus_tracer
from opencensus.trace.file_exporter import FileExporter
from opencensus.trace.tracer import Tracer, samplers

from src.config import ENVIRONMENT, GCP_PROJECT, TRACE_SAMPLING_RATE


def init_tracer(project_id=GCP_PROJECT):
    sampler = samplers.ProbabilitySampler(TRACE_SAMPLING_RATE)

    if ENVIRONMENT in {"stg", "prod"}:
        exporter = StackdriverExporter(project_id=project_id, transport=AsyncTransport)
    else:
        exporter = FileExporter(transport=AsyncTransport)

    tracer = Tracer(sampler=sampler, exporter=exporter)
    return tracer


def get_frame_name(back=1):
    frame = inspect.currentframe()
    for _ in range(back):
        frame = frame.f_back

    name = []

    module = inspect.getmodule(frame)
    if module is not None:
        name.append(module.__name__)

    if "self" in frame.f_locals:
        name.append(frame.f_locals["self"].__class__.__qualname__)

    code_name = frame.f_code.co_name
    if code_name != "<module>":
        name.append(code_name)

    del frame
    return ".".join(name)


def get_function_name(func):
    name = [func.__qualname__]

    module = inspect.getmodule(func)
    if module is not None:
        name.insert(0, module.__name__)

    return ".".join(name)


@contextmanager
def start_trace_span(suffix="", span_name=None, f_back=3):
    span_name = get_frame_name(f_back) if span_name is None else span_name
    span_name = span_name + suffix
    with get_opencensus_tracer().span(span_name) as scope:
        yield scope


def trace_function(func=None, name=None):
    if func is None:
        return functools.partial(trace_function, name=name)

    span_name = name if name else get_function_name(func)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with get_opencensus_tracer().span(span_name):
            return func(*args, **kwargs)

    return wrapped
