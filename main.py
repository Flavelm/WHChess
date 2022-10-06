request_error = '{"Error":"RequestError"}'
try:#Измени очерёдность ходов
	import traceback
	from flask import Flask, request
	import pretty_errors
	from Room import RoomsClass
	from Player import PlayersSave
	from funcs import IsNone
	from threading import Thread
except:
	print("Import Error")
	input(traceback.format_exc())
app = Flask("The_EnG1nE server")

def ReGet(key:str, default=None):
	return request.headers.get(key, default)

@app.route("/")
def GoToNah():
	return '<a href="https://discord.gg/crSZCMvRbQ">Discord сервер для загрузки клиента</a>\n<a href="https://www.youtube.com/c/TheEnG1eNbaHHbaSh_OR1G1NAJL">YouTube</a>\n<h1>Ололо ололо, я водитель НЛО</h1>'

@app.route("/login", methods = ["GET", "POST"])
def Login():
	Nickname = ReGet("nick")
	Password = ReGet("pass")
	Platform = ReGet("platform")
	if IsNone(Nickname, Password, Platform):
		return request_error
	return Players.login(Nickname, Password, Platform)

@app.route("/show", methods = ["GET", "POST"])
def show4mouse():
	RoomName = ReGet("roomname")
	if IsNone(RoomName):
		return request_error
	return Rooms.show4mouse(RoomName)

@app.route("/move", methods = ["GET", "POST"])
def Move():
	id = ReGet("id")
	RoomName = ReGet("roomname")
	startpos = ReGet("startpos")
	endpos = ReGet("endpos")
	if IsNone(RoomName, startpos, endpos):
		return request_error
	return Rooms.Move(startpos, endpos, RoomName, id)

@app.route("/register", methods = ["GET", "POST"])
def Register():
	Nickname = ReGet("nick")
	Password = ReGet("pass")
	if IsNone(Nickname, Password):
		return request_error
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
	mode = ReGet("mode", "classic")
	Reversed = ReGet("reverse", False)
	MaxPlayers = int(ReGet("maxplayers", 2))
	if IsNone(RoomName, IdPlayer):
		return request_error
	Reversed = bool(int(Reversed))
	return str(Rooms.CreateRoom(IdPlayer, RoomName, mode, Reversed, MaxPlayers))
@app.route("/join", methods = ["GET", "POST"])
def JoinToRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return request_error
	return str(Rooms.JoinToRoom(IdPlayer, RoomName))

@app.route("/leave", methods = ["GET", "POST"])
def LeaveFromRoom():
	IdPlayer = ReGet("id")
	RoomName = ReGet("roomname")
	if IsNone(RoomName, IdPlayer):
		return request_error
	return str(Rooms.LeaveFromRoom(IdPlayer, RoomName))

Players = PlayersSave()
Rooms = RoomsClass()
app.run(host='0.0.0.0')