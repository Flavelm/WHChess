"""
from requests import get
get("http://127.0.0.1:5000/join", headers = {"nick":"mouse", "pass":"zxcmouse", "id":"8640", "roomname":"Fun", "platform":"PythonConsole", "startpos":"e2", "endpos":"e4"}).text
"""
from os import system
import traceback
from requests import get
idplayer = input("id ")
while 1:
    try:
        address = input("Введите адресс ")
        if address == "move":
            pos = input("Координаты ").split(" ")
        elif address == "cls":
            system("cls")
        elif address == "show":
            ChessBoard = get(f"http://127.0.0.1:5000/show", headers = {"nick":"Nya", "fog":"True", "color":input("Цвет "), "random":"True", "pass":"Me0w", "id":idplayer, "roomname":"Fun", "platform":"PythonConsole", "startpos":pos[0], "endpos":pos[1]}).text
            Pole = str(ChessBoard)
            Pole = Pole.replace("'",'"')
            Pole = Pole.replace('"',"")
            Pole = Pole.replace(", ","")
            Pole = Pole.replace("],","\n")
            Pole = Pole.replace("[","")
            Pole = Pole.replace("]","\n")
            Pole = Pole.replace("White king","1")
            Pole = Pole.replace("White queen", "2")
            Pole = Pole.replace("Black king","0")
            Pole = Pole.replace("Black queen", "9")
            Pole = Pole.replace("White knight","3")
            Pole = Pole.replace("Black knight", "8")
            Pole = Pole.replace("White castle", "4")
            Pole = Pole.replace("Black castle", "7")
            Pole = Pole.replace("Black bishop", "5")
            Pole = Pole.replace("White bishop", "6")
            Pole = Pole.replace("White pawn", "w")
            Pole = Pole.replace("Black pawn", "b")
            Pole = Pole.replace("null", "♂")
            Pole = Pole.replace("fog", "♀")
            pole = ""
            
            for symb in Pole:
                pole += symb + " "
            Pole = "Партия в комнате " + "Ъуь" + "\n " + pole
            print(Pole)
            continue
        else:
            pos = ["e2", "e4"]
        print("\n", get(f"http://127.0.0.1:5000/{address}", headers = {"nick":"Nya", "free":"False", "fog":"True", "random":"True", "pass":"Me0w", "id":idplayer, "roomname":"Fun", "platform":"PythonConsole", "startpos":pos[0], "endpos":pos[1]}).text)
    except:
        print(traceback.format_exc())