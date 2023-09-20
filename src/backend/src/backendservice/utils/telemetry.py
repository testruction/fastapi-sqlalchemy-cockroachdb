from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor


def init_tracer(args):
    """
    Tracing configuration using OpenTelemetry
    """
    resource = Resource.create(attributes={"service.namespace": "io.testruction",
                                           "service.name": "webdemo"})

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)

    otlp_exporter = OTLPSpanExporter()
    otlp_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(otlp_processor)

    trace.set_tracer_provider(provider)

    if args.trace_stdout:
        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter()))

    if args.database_engine == "sqlite":
        SQLite3Instrumentor().instrument()
    elif args.database_engine == "cockroachdb":
        Psycopg2Instrumentor().instrument(enable_commenter=False, skip_dep_check=True)
