KivyV = "1.0"
UnityV = "1.0"
RequestError = {"Error":"RequestError"}
#Вова, работай
try:#Измени очерёдность ходов
	import traceback, os
	from flask import Flask, request, redirect, url_for
	from Room import RoomsClass
	from Player import PlayersSave
	from funcs import IsNone, ВсеДанныеИзСписка, NotHeaders
	import json
	from copy import deepcopy
except:
	print("Import Error")
	input(traceback.format_exc())
app = Flask("The_EnG1nE server", static_folder="", template_folder="")

@app.route("/getVkivy", methods = ["GET", "POST"])
def GetPythonVersion():
	return KivyV

@app.route("/getVunity", methods = ["GET", "POST"])
def GetUnityVersion():
	return UnityV

def saveLdata():
	with open("Logos.data","w") as file: json.dump(ldata,file);

def ReGet(key:str, default=None) -> (str | None):
	return request.headers.get(key, default)

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
		return NotHeaders(Nickname, Password, Platform)
	return Players.login(Nickname, Password, Platform)

@app.route("/show", methods = ["GET", "POST"])
def show4mouse():
	RoomName = ReGet("roomname")
	id = ReGet("id")
	if IsNone(RoomName):
		return NotHeaders(RoomName)
	return Rooms.show4mouse(RoomName, id)

@app.route("/moves", methods = ["GET", "POST"])
def Moves(self):
	RoomName = ReGet("roomname")
	if IsNone(RoomName):
		return NotHeaders(RoomName)
	return Rooms.GetHistory(RoomName)
	

@app.route("/show/common", methods = ["GET", "POST"])
def showC():
	RoomName = ReGet("roomname")
	id = ReGet("id")
	if IsNone(RoomName):
		return NotHeaders(RoomName)
	return Rooms.showcommon(RoomName, id)

@app.route("/move", methods = ["GET", "POST"])
def Move():
	id = ReGet("id")
	RoomName = ReGet("roomname")
	startpos = ReGet("startpos")
	endpos = ReGet("endpos")
	if IsNone(RoomName, startpos, endpos, id):
		return NotHeaders(RoomName, startpos, endpos, id).replace("'", "\"")
	startpos = startpos.lower()
	endpos = endpos.lower()
	return str(Rooms.Move(startpos, endpos, RoomName, id)).replace("'","\"")

@app.route("/register", methods = ["GET", "POST"])
def Register():
	Nickname = ReGet("nick")
	Password = ReGet("pass")
	if IsNone(Nickname, Password):
		return NotHeaders(Nickname, Password)
	return Players.register(Nickname, Password)

@app.route("/rooms", methods = ["GET", "POST"])
def GetRooms():
	d = Rooms.RoomsReturn()
	return d

@app.route("/room", methods = ["GET", "POST"])
def GetRoom():
	RoomName = ReGet("roomname", "RoomName")
	return Rooms.RoomReturn(RoomName)

@app.route("/room/color", methods = ["GET", "POST"])
def GetColorFromRoom():
	PlayerId = ReGet("id")
	RoomName = ReGet("roomname")
	return Rooms.RoomGetColor(RoomName, PlayerId)

@app.route("/create", methods = ["GET", "POST"])
def CreateRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	free = ReGet("free", "0")
	random = ReGet("random", "0")
	WarFog = ReGet("fog", "0")
	Reversed = ReGet("reverse", "0")#color
	MaxPlayers = ReGet("maxplayers", "2")
	#MaxPlayers = int(ReGet("maxplayers", 2))
	if IsNone(RoomName, IdPlayer):
		return NotHeaders(RoomName, IdPlayer)
	mods = []
	for mode in [free, random, WarFog, Reversed]:
		mode = str(mode).lower()
		if  mode == "t"  or mode == "true"  or mode == "1": mods.append(1)
		elif mode == "f" or mode == "false" or mode == "0": mods.append(0)
		elif len(mode) == 1: mods.append(int(deepcopy(mode)))
	return Rooms.CreateRoom(IdPlayer, RoomName, {"free":mods[0], "random":mods[1], "fog":mods[2]}, mods[3], int(MaxPlayers))

@app.route("/join", methods = ["GET", "POST"])
def JoinToRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return NotHeaders(RoomName, IdPlayer)
	return Rooms.JoinToRoom(IdPlayer, RoomName)

@app.route("/leave", methods = ["GET", "POST"])
def LeaveFromRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return NotHeaders(RoomName, IdPlayer)
	return Rooms.LeaveFromRoom(IdPlayer, RoomName)

@app.route("/chat/get", methods = ["GET", "POST"])
def GetChat():
	RoomName = ReGet("roomname")
	if IsNone(RoomName):
		return(NotHeaders(RoomName))
	return Rooms.GetChat(RoomName)

@app.route("/chat/send", methods = ["GET", "POST"])
def SendMessage():
	RoomName = ReGet("roomname")
	PlayerId = ReGet("id")
	Message =  ReGet("message")
	if Message == "": Message = None
	if IsNone(RoomName):
		return(NotHeaders(RoomName))
	return Rooms.SendMessage(Message, PlayerId, RoomName)

@app.route("/notifications/player", methods = ["GET", "POST"])
def Player():
	IdPlayer = ReGet("id")
	if IsNone(IdPlayer):
		return RequestError
	return Players.GetNotification(IdPlayer)

@app.route("/notifications/send_all", methods = ["GET", "POST"])
def SellNotificationForAll():
	Pass = ReGet("pass")
	Message = ReGet("message")
	if IsNone(Pass, Message):
		return RequestError
	if Pass != "********":
		return "PassError"
	NickList = ВсеДанныеИзСписка("nick", Players.Players())
	for i in NickList:
		Players.AddNotifications(i, {"type":"server", "description":Message})
	return "1"

@app.route("/notifications/del_all", methods = ["GET", "POST"])
def DelNotif():
	PlayerId = ReGet("id")
	if IsNone(PlayerId):
		return RequestError
	return Players.DelAllNotification(PlayerId)

@app.route("/status", methods = ["GET","POST"])
@app.route("/profile", methods = ["GET","POST"])
def GetProfile(*_):
	Id = ReGet("id")
	if IsNone(Id):
		return RequestError
	return Players.GetProfile(Id)

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
	return "{\"None\": null}"

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
		return "Уровень с таким названием уже существует"
	lvl = ReGet("lvl")
	try:
		lvl = json.loads(lvl)
	except:return "Данные не являются уровнем"
	UserName = ReGet("nick");
	if leq(lvl): return "Уровень уже существует"
	ldata["lvls"][lvlName] = {"lvl":lvl, "owner":UserName};
	saveLdata();
	IsNone(UserName, lvlName, lvl)
	return "Успешно"

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
	except: return "error"

@app.route("/logoslvls", methods = ["POST","GET"])
def Loloslvls(*_):
	return ldata["lvls"]

@app.errorhandler(500)
def Error(*_):
	return {"Error":str(traceback.format_exc()).replace("\n"," ")}

@app.after_request
def add_header(response):
	response.headers["access-control-allow-origin"] = '*'
	response.headers["Access-Control-Allow-Origin"] = '*'
	response.headers["Content-Type"] = "text/plain"
	response.headers["Access-Control-Allow-Headers"] = "*"
	return response

Players = PlayersSave();
Rooms = RoomsClass();
app.run(host="0.0.0.0", port=8080);