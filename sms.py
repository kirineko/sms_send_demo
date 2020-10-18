import requests
from setting import API_KEY

def sms_send(mobile, code):
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    data = {
        'apikey': API_KEY,
        'mobile': mobile,
        'text': '您的验证码是{}, 请在2分钟内完成注册。'.format(code)
    }
    res = requests.post(url, data)
    print(res.json())