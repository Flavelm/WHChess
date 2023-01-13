RequestError = str({"Error":"RequestError"})
#Вова, работай
try:#Измени очерёдность ходов
	import traceback
	from flask import Flask, request, redirect, url_for
	from Room import RoomsClass
	from random import randint
	from Player import PlayersSave
	from funcs import IsNone, ВсеДанныеИзСписка
	import json
except:
	print("Import Error")
	input(traceback.format_exc())
app = Flask("The_EnG1nE server")

def saveLdata():
	with open("Logos.data","w") as file: json.dump(ldata,file);

def ReGet(key:str, default=None):
	return request.headers.get(key, default)

frass = ["Кто двинется, тот гей.","Лучше 5 см спереди,\nчем учить assembler", "UTF-8 not supported","","Вы думали я забыл?\nНо нет! Я забыл.", "500 Internal Server Error", "Вова работай!","Достаём двойные листочки","-40°C"]

ldata = {"Users":{}, "lvls":{}};

try:
	with open("Logos.data","r") as file: ldata = json.load(file);
except Exception as E: print(E);

@app.route("/ChessPage")
def GoToNah():
	return '<a href="https://discord.gg/crSZCMvRbQ">Discord сервер для загрузки клиента</a>\n<h1>ЬУЬ</h1>\n<a href="https://www.youtube.com/c/TheEnG1eNbaHHbaSh_OR1G1NAJL">YouTube</a>\n<h1>Ололо ололо, я водитель НЛО</h1>'

@app.route("/login", methods = ["GET", "POST"])
def Login():
	Nickname = ReGet("nick")
	Password = ReGet("pass")
	Platform = ReGet("platform")
	if IsNone(Nickname, Password, Platform):
		return RequestError
	d = Players.login(Nickname, Password, Platform)
	print(d)
	return d

@app.route("/show", methods = ["GET", "POST"])
def show4mouse():
	RoomName = ReGet("roomname")
	Color = ReGet("color", "qwertyuiop")
	Color = Color.lower()
	if IsNone(RoomName):
		return RequestError
	if Color == "white" or Color == "black":
		if Color == "white": Color = "White"
		else: Color = "Black"
		return Rooms.show4mouse(RoomName, Color)
	if Color == "qwertyuiop":
		return Rooms.show4mouse(RoomName)
	return {"Canvas":0, "description":"Color must be White or Black"}

@app.route("/move", methods = ["GET", "POST"])
def Move():
	id = ReGet("id")
	RoomName = ReGet("roomname")
	startpos = ReGet("startpos")
	endpos = ReGet("endpos")
	if IsNone(RoomName, startpos, endpos):
		return RequestError
	d = Rooms.Move(startpos, endpos, RoomName, id)
	print(d)
	return d

@app.route("/register", methods = ["GET", "POST"])
def Register():
	Nickname = ReGet("nick")
	Password = ReGet("pass")
	if IsNone(Nickname, Password):
		return RequestError
	return Players.register(Nickname, Password)

@app.route("/rooms", methods = ["GET", "POST"])
def GetRooms():
	return str(Rooms.RoomsReturn())

@app.route("/room", methods = ["GET", "POST"])
def GetRoom():
	RoomName = ReGet("roomname")
	return str(Rooms.RoomReturn(RoomName))

@app.route("/room/color", methods = ["GET", "POST"])
def GetColorFromRoom():
	PlayerId = ReGet("id")
	RoomName = ReGet("roomname")
	return str(Rooms.RoomGetColor(RoomName, PlayerId))

@app.route("/create", methods = ["GET", "POST"])
def CreateRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	free = ReGet("free", "False")
	random = ReGet("random", "False")
	WarFog = ReGet("fog", "False")
	Reversed = ReGet("reverse", False)#color
	MaxPlayers = int(ReGet("maxplayers", 2))
	if IsNone(RoomName, IdPlayer):
		return RequestError
	Reversed = bool(int(Reversed))
	return str(Rooms.CreateRoom(IdPlayer, RoomName, {"free":free, "random":random, "fog":WarFog}, Reversed, MaxPlayers))

@app.route("/join", methods = ["GET", "POST"])
def JoinToRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return RequestError
	return str(Rooms.JoinToRoom(IdPlayer, RoomName))

@app.route("/leave", methods = ["GET", "POST"])
def LeaveFromRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return RequestError
	return str(Rooms.LeaveFromRoom(IdPlayer, RoomName))

@app.route("/notifications/player", methods = ["GET", "POST"])
def Player():
	IdPlayer = ReGet("id")
	if IsNone(IdPlayer):
		return RequestError
	return str(Players.GetNotification(IdPlayer))

@app.route("/notifications/send_all", methods = ["GET", "POST"])
def SellNotificationForAll():
	Pass = ReGet("pass")
	Message = ReGet("message")
	if IsNone(Pass, Message):
		return RequestError
	if Pass != "********":
		return "PassError"
	NickList = ВсеДанныеИзСписка("nick", Players.Players)
	for i in NickList:
		Players.AddNotifications(i, {"type":"server", "description":Message})
	return "1"

@app.route("/send", methods=["POST"])
def Cummentariy():
    if request.form.get("spam", "f") != "f":
        return ToMainPage()
    Nick = request.form.get("Nickname", "")
    Cum  = request.form.get("comment", "")
    if Nick == "" or Cum == "":
        return ToMainPage()
    print(f"{Nick}:", Cum)
    return ToMainPage()

@app.route("/printe", methods=["POST", "GET"])
def ppr(*_):
	print(ReGet("m"))
	return ""

@app.route("/")
def ToMainPage(*_):
    return redirect(url_for("MainPage"))

@app.route("/llogin", methods = ["POST","GET"])
def llogin():
	UserName = ReGet("nick");
	UserPassword = ReGet("pass");
	if UserName in ldata["Users"]:
		if ldata["Users"][UserName] == UserPassword:return "1"
		else:return "0"
	else:return "0"

@app.route("/checkversion", methods = ["POST", "GET"])
def vers(*_):
	return "1.0"

@app.route("/lreg", methods = ["POST", "GET"])
def lreg():
	UserName = ReGet("nick");
	UserPass = ReGet("pass");
	if UserName in ldata["Users"]:
		return "Ник занят"
	ldata["Users"][UserName] = UserPass;
	saveLdata();
	return "Вы успешно зарегистрировались"

def lvleq(lvl, slvl):
	print(lvl, slvl)
	for x in range(len(lvl)):
		for y in range(len(lvl)):
			if lvl[x][y] != slvl[x][y]: return False
	return True
def leq(lvl):
	for slvl in ldata["lvls"]:
		slvl = ldata["lvls"][slvl]["lvl"]
		print("l1",lvl,"\nl2", slvl);
		if len(lvl) == len(slvl):
			if lvleq(lvl, slvl):
				return True
	return False

@app.route("/addlogoslvl", methods = ["POST","GET"])
def AddLvl(*_):
	lvlName = ReGet("name")
	if lvlName in ldata["lvls"]:
		return "Уровень с таким названием уже существует";
	lvl = ReGet("lvl")
	try:
		lvl = json.loads(lvl)
	except:return "Данные не являются уровнем";
	UserName = ReGet("nick");
	if leq(lvl): return "Уровень уже существует"
	ldata["lvls"][lvlName] = {"lvl":lvl, "owner":UserName};
	saveLdata();
	IsNone(UserName, lvlName, lvl)
	return "Успешно";

@app.route("/dellvl", methods=["POST","GET"])
def DelLvl(*_):
	UserName = ReGet("nick")
	Level = ReGet("name")
	if not Level in ldata["lvls"]: return "0"
	if ldata["lvls"][Level]["owner"] == UserName:
		ldata["lvls"].pop(Level);
		saveLdata();
		return "1"
	return "0"

@app.route("/card", methods=["POST","GET"])
def Card(*_):
	try:
		with open("mcard","r") as f:
			return f.read()
	except: return "error";

@app.route("/logoslvls", methods = ["POST","GET"])
def Loloslvls(*_):
	return ldata["lvls"];

@app.route("/MainPage")
def MainPage():
    return '''<!DOCTYPE html>

<head><title>Основной сайт сервера</title></head>
<body>
    <style>
        *{
            padding: 0;
            margin: 0;
        }
        .border {
            padding: 2%;
            text-align: center;
        }
        .anim {
            -webkit-animation: scale-up-hor-center 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
                    animation: scale-up-hor-center 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
        }
        .gradient{background: linear-gradient(to bottom right, rgb(189, 129, 0), rgb(170, 0, 0)); background-size: cover; min-height:100vh;}
		h2{color: white}
        h1{color: whitesmoke;}
        a{color: rgb(218, 218, 255);}
        li{color: red;}
        .y{-webkit-animation:roll-in-top 5s ease-in-out infinite alternate both;animation:roll-in-top 5s ease-in-out infinite alternate both}
        @-webkit-keyframes roll-in-top{0%{-webkit-transform:translateY(-800px) rotate(-540deg);transform:translateY(-800px) rotate(-540deg);opacity:0}100%{-webkit-transform:translateY(0) rotate(0deg);transform:translateY(0) rotate(0deg);opacity:1}}@keyframes roll-in-top{0%{-webkit-transform:translateY(-800px) rotate(-540deg);transform:translateY(-800px) rotate(-540deg);opacity:0}100%{-webkit-transform:translateY(0) rotate(0deg);transform:translateY(0) rotate(0deg);opacity:1}}
        @-webkit-keyframes scale-up-hor-center {
            0% {
                -webkit-transform: scaleX(0.4);
                        transform: scaleX(0.4);
            }
            100% {
                -webkit-transform: scaleX(1);
                        transform: scaleX(1);
            }
            }
            @keyframes scale-up-hor-center {
            0% {
                -webkit-transform: scaleX(0.4);
                        transform: scaleX(0.4);
            }
            100% {
                -webkit-transform: scaleX(1);
                        transform: scaleX(1);
            }
            }
    </style>
    <div class="gradient">
        <div class="y"><h2>Жизненные фразы:\n"'''+ frass[randint(0,len(frass)-1)] +'''"</h2></div>
        <div class="border">
            <img src='https://i.pinimg.com/564x/8e/54/b1/8e54b114023bca08d4c23b620adef809.jpg' align = "right">
                <div class="anim">
                <h1>Куда надо?</h1>
                <li>
                    <a href="/ChessPage">Шахматы</a>
                </li>
                <form action="/send", method="post">
                    <input type="text" name="Nickname" placeholder="Ник">
                    <input type="text" name="comment" placeholder="Cumментарий">
                    <input type="checkbox" name="spam" value="t"> Спам
                    <input type="submit" value="Отправить">
                </form>
				
                </div>
            </div>
        <div class="border">
            <a href="https://discord.gg/crSZCMvRbQ"><img src="https://upload.wikimedia.org/wikipedia/ru/thumb/b/b7/Discord_logo_svg.svg/2560px-Discord_logo_svg.svg.png" width="400" height="70"></a>
            <a href="https://www.youtube.com/c/TheEnG1eNbaHHbaSh_OR1G1NAJL"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/2560px-YouTube_full-color_icon_%282017%29.svg.png" width="150" height="100"></a>
        </div>
            
        
    </div>
</body>'''

Players = PlayersSave()
print(Players.Players)
Rooms = RoomsClass()
app.run(host='0.0.0.0')