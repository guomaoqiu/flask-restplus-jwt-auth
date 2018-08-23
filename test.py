import requests
from fake_useragent import UserAgent

ua = UserAgent()
print(ua.random)
print(ua.random)
print(ua.random)

while True:
    url = 'http://ferland.h5.sinreweb.com/activity2/ferland.microvote.api/vote?activity_id=1'

    head = {
        "Host" : "ferland.h5.sinreweb.com",
        "User-Agent" : ua.random,
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding" : "gzip, deflate",
        "Referer" : "http://ferland.h5.sinreweb.com/micro_vote/?player_id=185&division_id=27&from=timeline&isappinstalled=0",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With" : "XMLHttpRequest",
        "Connection" : "keep-alive"
    }


    postData = {
        "id" : 185
    }
    print(ua.random)
    import time,random
    randmo=random.randint(0,60)
    print(randmo)
    time.sleep(randmo)
    rsp = requests.post(url, headers=head, data=postData)
    print(rsp.content.decode("utf-8"))