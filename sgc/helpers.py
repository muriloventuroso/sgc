import os
import re


def get_mongo_url():
    if 'MONGODB_URI' in os.environ:
        url = os.environ['MONGODB_URI']
        m = re.match(r"^mongodb:\/\/(?:(?:(\w+)?:(\w+)?@)|:?@?)((?:[\w.-])+)(?::(\d+))?(?:\/([\w-]+))?(?:\?([\w-]+=[\w-]+(?:&[\w-]+=[\w-]+)*)?)?$", url)
        if m:
            return {'USER': m.group(1), 'PASSWORD': m.group(2), 'HOST': m.group(3), 'PORT': int(m.group(4)), 'NAME': m.group(5)}
    return {}


def get_cache():
    import os
    try:
        servers = os.environ['MEMCACHIER_SERVERS']
        username = os.environ['MEMCACHIER_USERNAME']
        password = os.environ['MEMCACHIER_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
                    # TIMEOUT is not the connection timeout! It's the default expiration
                    # timeout that should be applied to keys! Setting it to `None`
                    # disables expiration.
                    'TIMEOUT': None,
                    'LOCATION': servers,
                    'OPTIONS': {
                      'binary': True,
                      'username': username,
                      'password': password,
                      'behaviors': {
                        # Enable faster IO
                        'no_block': True,
                        'tcp_nodelay': True,
                        # Keep connection alive
                        'tcp_keepalive': True,
                        # Timeout settings
                        'connect_timeout': 2000, # ms
                        'send_timeout': 750 * 1000, # us
                        'receive_timeout': 750 * 1000, # us
                        '_poll_timeout': 2000, # ms
                        # Better failover
                        'ketama': True,
                        'remove_failed': 1,
                        'retry_timeout': 2,
                        'dead_timeout': 30,
                      }
                    }
                }
            }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': '127.0.0.1:11211',
                'TIMEOUT': 60,  # Default: 300 segundos,
                'KEY_PREFIX': 'djcache',
            }
        }