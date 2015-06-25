import os
import sys
import logging
import logging.handlers
import socket


class DefaultConfig(object):
    """
    Configuration suitable for use for development
    """
    DEBUG = bool(os.getenv('DEBUG', True))
    APPLICATION_ROOT = os.getenv('APPLICATION_ROOT')
    JSONIFY_PRETTYPRINT_REGULAR = bool(os.getenv('JSONIFY_PRETTYPRINT_REGULAR', True))

    STATIC_ENABLED_ENVS = set(os.getenv('STATIC_ENABLED_ENVS', 'dev test').split(' '))

    TILE_INDEX_FILES = {
        "desktop": "/var/data/onyx/desktop_tile_index.json",
        "desktop-prerelease": "/var/data/onyx/desktop-prerelease_tile_index.json",
        "android": "/var/data/onyx/android_tile_index.json"
    }

    ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

    # defaults to {'desktop':None,'desktop-prerelease':None,'android':None}
    # env format is LINKS_LOCALIZATIONS='key1=value1 key2= key3=value3' which
    # converts to {'key1': 'value1', 'key2': None, 'key3': 'value3'}
    LINKS_LOCALIZATIONS = {
        key: (value or None)
        for pair in os.getenv(
            'LINKS_LOCALIZATIONS',
            'desktop= desktop-prerelease= android=',
        ).split(' ')
        for key, value in [pair.split('=')]
    }

    GEO_DB_FILE = os.getenv(
        'GEO_DB_FILE',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/GeoLite2-Country.mmdb")
    )

    STATSD = {
        'host': os.getenv('STATSD_HOST', '127.0.0.1'),
        'port': int(os.getenv('STATSD_PORT', 8125),
    }

    LOG_HANDLERS = {
        'application': {
            'handler': logging.handlers.SysLogHandler,
            'level': logging.INFO,
            'params': {
                'address': ('localhost', 514),
                'facility': logging.handlers.SysLogHandler.LOG_LOCAL0,
                'socktype': socket.SOCK_DGRAM,
            }
        },
        'client_error': {
            'handler': logging.handlers.SysLogHandler,
            'level': logging.INFO,
            'params': {
                'address': ('localhost', 514),
                'facility': logging.handlers.SysLogHandler.LOG_LOCAL1,
                'socktype': socket.SOCK_DGRAM,
            }
        },
        'user_event': {
            'handler': logging.handlers.SysLogHandler,
            'format': '%(message)s',
            'level': logging.INFO,
            'params': {
                'address': ('localhost', 514),
                'facility': logging.handlers.SysLogHandler.LOG_LOCAL2,
                'socktype': socket.SOCK_DGRAM,
            }
        },
        'console': {
            'handler': logging.StreamHandler,
            'level': logging.DEBUG,
            'params': {
                'stream': sys.stdout
            }
        },
    }
