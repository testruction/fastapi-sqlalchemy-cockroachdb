from fastapi import Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import (ConsoleSpanExporter,
                                            SimpleSpanProcessor,
                                            BatchSpanProcessor)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from frontendservice.utils.userid import get_openid_user


def init_tracer(args):
    """
    Tracing configuration using OpenTelemetry
    """
    resource = Resource.create(attributes={"service.namespace": "io.testruction",
                                           "service.name": "webdemo"})

    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter()
    otlp_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(otlp_processor)

    trace.set_tracer_provider(provider)

    if args.trace_stdout:
        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(
                ConsoleSpanExporter()
                )
            )

    # https://pypi.org/project/opentelemetry-instrumentation-httpx/
    def request_hook(span: trace.get_current_span(), request):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user(Request))

    def response_hook(span: trace.get_current_span(), request, response):
        pass

    HTTPXClientInstrumentor().instrument(request_hook=request_hook,
                                         response_hook=response_hook)
