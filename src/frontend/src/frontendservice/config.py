# -*- coding: utf-8 -*-
import os
import argparse

from frontendservice.utils.logging import init_logger
from frontendservice.utils.telemetry import init_tracer

# CLI arguments composition
parser = argparse.ArgumentParser()
parser.add_argument('--debug',
                    help='Enable debug logging',
                    action='store_true')
parser.add_argument('--trace-stdout',
                    help="Show OpenTelemetry output to console",
                    action="store_true")
parser.add_argument('--backend-api-url',
                    type=str,
                    help='Hostname, fully qualified name or IP address',
                    default=os.environ.get('BACKEND_API_URL',
                                           default='http://backend:8000'))
args, unknown = parser.parse_known_args()

# Initialize logging
init_logger(args)
# Initialize telemetry
init_tracer(args)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_NABLED = True
    SITE_NAME = 'webdemo-frontendservices'
    SECRET_KEY = os.urandom(32)

    JSON_SORT_KEYS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
