import bottle
import redis
import random
from sms import sms_send
from response import info, suss, fail


r = redis.StrictRedis()

def limit_rate(func):
    def api(*args, **kwagrs):
        ip = bottle.request.remote_addr
        name = func.__name__
        key = 'limit:rate:{}:{}'.format(ip, name)
        if r.exists(key):
            rate = r.incr(key)
            if rate > 10:
                return fail('IP:{}, 访问频率过高'.format(ip))
            return func(*args, **kwagrs)
        
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, 60)
        pipe.execute()
        return func(*args, **kwagrs)
    return api


@bottle.get('/api')
@limit_rate
def api():
    return suss('正常接口')

@bottle.get('/')
def index():
    bottle.redirect('/signup')

@bottle.get('/signup')
@bottle.view('signup')
def signup():
    return dict()

@bottle.post('/getcode')
@limit_rate
def getcode():
    mobile = bottle.request.forms['mobile']
    code = random.randint(100000, 999999)
    
    sms_send(mobile, code)

    key = 'sms:{}'.format(mobile)
    pipe = r.pipeline()
    pipe.set(key, code)
    pipe.expire(key, 180)
    pipe.execute()
    return suss(mobile)

@bottle.post('/signup')
def signup():
    mobile = bottle.request.forms['mobile']
    code = bottle.request.forms['code']
    key = 'sms:{}'.format(mobile)

    if r.exists(key):
        sms_code = r.get(key).decode('utf-8')
        if sms_code == code:
            r.delete(key)
            return suss('注册成功')
        return fail('验证码不一致')
    return fail('验证码已经过期')

bottle.run(reloader=True)