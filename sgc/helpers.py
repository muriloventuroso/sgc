import os
import re
from django.shortcuts import redirect


def get_mongo_url():
    if 'MONGODB_URI' in os.environ:
        url = os.environ['MONGODB_URI']
        print(url)
        return {'HOST': url}
    return {}


def get_cache():
    import os
    try:
        servers = os.environ['MEMCACHEDCLOUD_SERVERS']
        username = os.environ['MEMCACHEDCLOUD_USERNAME']
        password = os.environ['MEMCACHEDCLOUD_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django_bmemcached.memcached.BMemcached',
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
                        'connect_timeout': 2000,  # ms
                        'send_timeout': 750 * 1000,  # us
                        'receive_timeout': 750 * 1000,  # us
                        '_poll_timeout': 2000,  # ms
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


def redirect_with_next(request, reverse):
    params = request.GET.copy()
    if 'next' in params and params['next'] == '/':
        response = redirect('home')
    else:
        response = redirect(reverse)
    response['Location'] += '?' + params.urlencode()
    return response
