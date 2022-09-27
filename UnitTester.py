from requests import get
get("http://127.0.0.1:5000/login", headers = {"nick":"Nya", "pass":"Me0w", "id":"1273", "roomname":"Fun", "platform":"PythonConsole", "startpos":"e2", "endpos":"e4"}).text