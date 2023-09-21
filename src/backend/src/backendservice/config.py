import os
import argparse

from sqlalchemy.engine import URL

from backendservice.utils.logging import init_logger
from backendservice.utils.telemetry import init_tracer

# CLI arguments composition
parser = argparse.ArgumentParser()
parser.add_argument('--debug',
                    help='Enable debug logging',
                    action='store_true')
parser.add_argument('--trace-stdout',
                    help="Show OpenTelemetry output to console",
                    action="store_true")
parser.add_argument('--database-engine',
                    type=str,
                    help='Database engine (cockroachdb, postgres, sqlite)',
                    default=os.environ.get('DATABASE_ENGINE', default='sqlite'))
parser.add_argument('--database-host',
                    type=str,
                    help='Hostname, fully qualified name or IP address',
                    default=os.environ.get('COCKROACH_HOST', default='localhost'))
parser.add_argument('--database-port',
                    type=int,
                    help='Listening port',
                    default=os.environ.get('COCKROACH_PORT', default=26257))
parser.add_argument('--database-username',
                    type=str,
                    help='Database user login name',
                    default=os.environ.get('COCKROACH_USER', default='root'))
parser.add_argument('--database-password',
                    type=str,
                    help='Database user login password',
                    default=os.environ.get('COCKROACH_PASSWORD', default='dummypassword'))
parser.add_argument('--database',
                    type=str,
                    help='Name of the database',
                    default=os.environ.get('COCKROACH_DB', default='postgres'))
args, unknown = parser.parse_known_args()

# Initialize logging and telemetry
init_logger(args)
init_tracer(args)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_NABLED = True
    SITE_NAME = 'app'
    SECRET_KEY = os.urandom(32)

    if args.database_engine == 'sqlite':
        SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite.db"
    elif args.database_engine == 'cockroachdb':
        SQLALCHEMY_DATABASE_URI = URL.create(drivername='cockroachdb',
                                             username=args.database_username,
                                             password=args.database_password,
                                             host=args.database_host,
                                             port=args.database_port,
                                             database=args.database)

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
