"""
from requests import get
get("http://127.0.0.1:5000/login", headers = {"nick":"mouse", "pass":"zxcmouse", "id":"8640", "roomname":"Fun", "platform":"PythonConsole", "startpos":"e2", "endpos":"e4"}).text
"""
from requests import get
while 1:
    address = input("Введите адресс ")
    if address == "move":
        pos = input("Координаты ").split(" ")
    else:
        pos = ["e2", "e4"]
    print("\n", get(f"http://127.0.0.1:5000/{address}", headers = {"nick":"Nya", "pass":"Me0w", "id":"434500411652890428", "roomname":"Fun", "platform":"PythonConsole", "startpos":pos[0], "endpos":pos[1]}).text)