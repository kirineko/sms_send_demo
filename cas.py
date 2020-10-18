import redis

r = redis.StrictRedis()

def incr(key):
    r.watch(key)
    val = r.get(key)
    if not val:
        val = 0
    val = int(val) + 1

    pipe = r.pipeline()
    pipe.set(key, val)
    pipe.execute()

def hsetnx(key, field, value):
    r.watch(key)
    is_field_exist = r.hexists(key, field)
    if not is_field_exist:
        pipe = r.pipeline()
        pipe.hset(key, field, value)
        pipe.execute()
    else:
        r.unwatch(key)
    return is_field_exist