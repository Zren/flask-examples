# Flask Examples

This repo contains the collective tips and tricks I've found while expirementing with Flask.

All examples are meant to be used on Heroku.

## Memcache

Add some microcaching (cache with fast timeout Eg: 5 seconds) between your gunicorn workers. Very useful if some of your routes fetch data from a 3rd party service where the data doesn't need to up to date.

I tend to use Windows for developing if I can help it. However, memcache is one of those tools that's a pain to setup on windows. `pylibmc` requires a compiler to install with `pip`. Let alone the `libmemcached` it binds to. I found `python-binary-memcached` which simplifies the process.

    cd memcache-example

Now install the dependancies.  
    pip install -r requirements.txt

We also need an actual memcache server to test on. Fortunately there's a free tier on Heroku. I used [Memcachier](https://addons.heroku.com/memcachier#dev).

    heroku addons:add memcachier

Since I'm not everyone is working on Windows, you could just install a local memcache server on my pc. That requires me to firer up a Linux VM however, which feels like overkill for a simple flask app. Instead, I set my local environment variables to the live memcachier servers.

We can get the values at with

    heroku config

    === ??? Config Vars
    MEMCACHIER_PASSWORD:   ??????????????????????????
    MEMCACHIER_SERVERS:    ???.dev.ec2.memcachier.com:11211
    MEMCACHIER_USERNAME:   ?????????

Just to make sure there's no errors popping up, I set the logging level to debug.

    import logging
    logging.basicConfig(level=logging.DEBUG)

### Flask-Cache

Now that we've set things up, we need to actually implment the memcache. Luckily there's already a module to simplify things with decorators.

http://pythonhosted.org/Flask-Cache/

Flask Cache doesn't come with an implementation for the `bmemcached` module (`python-binary-memcached`). We just need to copy what was done for the built in SASLMemcachedCache which runs on `pylibmc`. You can check it out in `flask_cache_backends.py`. Custom backends are required to be in their own module as it only flagged as custom if it has a `.` in it. It's then loaded with [werkzeug.utils.import_string](http://werkzeug.pocoo.org/docs/utils/#werkzeug.utils.import_string).


After it's all setup, it's dead easy to use.

    @app.route('/')
    @cache.cached(timeout=MICROCACHE_TIMEOUT)
    def index():
        from datetime import datetime
        return datetime.now().isoformat()

One thing you might run into is that @cache.memoize() doesn't memoize the query string parameters. There's solution for this on StackOverflow.

https://stackoverflow.com/questions/9413566/flask-cache-memoize-url-query-string-parameters-as-well/14264116#14264116
