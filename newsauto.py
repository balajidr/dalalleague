import time
import urllib.request
import requests
import random


#
# def executeSomething():
#     with urllib.request.urlopen('http://localhost:5003/setNews?company=Gaggle&value={}'.format(random.randint(1,5))) as response:
#         html = response.read()
#         print(html)


def dosomething():
    li = ['Babur', 'Emptyhad', 'Gaggle', 'Loyalenfield', 'Mapple', 'Rexxon', 'Smokacola']
    ran = random.randint(1, 7)
    l = li[ran - 1]
    r = requests.get('http://localhost:5003/setNews?company={}&value={}'.format(l, random.randint(1, 5)))
    print(r.text)
    print(r.status_code, r.reason)


while True:
    #executeSomething()
    dosomething()
    time.sleep(4)  #set time

