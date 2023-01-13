from threading import Thread as run
from time import time as t, sleep as delay
from random import randint as ri
from requests import get as g

g("http://217.106.107.85:5000/MainPage", headers={"ок":"хуй"}).text 

def RandomElement(ellist:list)->str:
    return ellist[ri(0, len(ellist)-1)]

def GenUserName():
    return RandomElement(["The_EnG1nE", "mv_mouse", "Lexa2008", "whitenigger"])

tstart = t()

Profiles = []
for i in range(1000):
    Profiles.append({"name" : GenUserName(), "messages":[]})

print("Создание 1000 акков заняло", t()-tstart, "В округении", round(t() - tstart))

tstart = t()
for i in range(100000):
    Profiles[0]["messages"].append({"ByUser":GenUserName(), "message":RandomElement(["Hi", "Privet", "Vova tupoy"])})

print("Написание 100000 сообщений заняло", t()-tstart, "В округении", round(t() - tstart))

tstart = t()
 
def send_mess(nick, message):
    g("http://217.106.107.85:5000/MainPage", headers={"Nickname":nick, "comment":message}).text

for i in Profiles[0]["messages"]:
    run(target=send_mess, args=(i["ByUser"], i["message"])).run()

print("Условное (+усложнённое) получение этих злоебучих сообщений (100000) заняло", t()-tstart, "В округении", round(t() - tstart))
print("Погрешность", t()-t())
input("Всё...")
