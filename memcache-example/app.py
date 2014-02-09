import os

import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask
from flask.ext.cache import Cache

# Constants
USE_MEMCACHE = True
MICROCACHE_TIMEOUT = 5 # 5 Seconds

# Init
## App
app = Flask(__name__)

## Cache
cache_config = {}
cache_config['CACHE_TYPE'] = 'simple'

### Memcache

if USE_MEMCACHE:
    username = os.environ.get('MEMCACHIER_USERNAME') or os.environ.get('MEMCACHE_USERNAME')
    password = os.environ.get('MEMCACHIER_PASSWORD') or os.environ.get('MEMCACHE_PASSWORD')
    servers = os.environ.get('MEMCACHIER_SERVERS') or os.environ.get('MEMCACHE_SERVERS')
    if username and password and servers:
        servers = servers.split(';')
        cache_config['CACHE_TYPE'] = 'flask_cache_backends.bmemcached'
        cache_config['CACHE_MEMCACHED_USERNAME'] = username
        cache_config['CACHE_MEMCACHED_PASSWORD'] = password
        cache_config['CACHE_MEMCACHED_SERVERS'] = servers
cache = Cache(app, config=cache_config)

# Routes
## Pages
@app.route('/')
@cache.cached(timeout=MICROCACHE_TIMEOUT)
def index():
    from datetime import datetime
    return datetime.now().isoformat()

# Main
if __name__ == '__main__':
    # Not used with gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
