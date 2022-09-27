request_error = '{"Error":"RequestError"}'
try:
	import traceback
	from flask import Flask, request
	from random import randint
	import pretty_errors
	from Room import RoomsClass
	from Player import PlayersSave
	from funcs import IsNone
except:
	print("Import Error")
	input(traceback.format_exc())
app = Flask("The_EnG1nE server")
@app.route("/login", methods = ["GET", "POST"])
def Login():
	Nickname = request.headers.get("nick")
	Password = request.headers.get("pass")
	Platform = request.headers.get("platform")
	if IsNone(Nickname, Password, Platform):
		return request_error
	return Players.login(Nickname, Password, Platform)

@app.route("/show4mouse", methods = ["GET", "POST"])
def show4mouse():
	RoomName = request.headers.get("roomname")
	if IsNone(RoomName):
		return request_error
	return Rooms.show4mouse(RoomName)

@app.route("/move", methods = ["GET", "POST"])
def Move():
	id = request.headers.get("id")
	RoomName = request.headers.get("roomname")
	startpos = request.headers.get("startpos")
	endpos = request.headers.get("endpos")
	if IsNone(RoomName, startpos, endpos):
		return request_error
	return Rooms.Move(startpos, endpos, RoomName, id)

@app.route("/show", methods = ["GET", "POST"])
def PrintingBoard():
	RoomName = request.headers.get("roomname")
	if IsNone(RoomName):
		return request_error
	return Rooms.PrintCanvas(RoomName)

@app.route("/register", methods = ["GET", "POST"])
def Register():
	Nickname = request.headers.get("nick")
	Password = request.headers.get("pass")
	if IsNone(Nickname, Password):
		return request_error
	return Players.register(Nickname, Password)

@app.route("/rooms", methods = ["GET", "POST"])
def GetRooms():
	return str(Rooms.RoomReturn())

@app.route("/create", methods = ["GET", "POST"])
def CreateRoom():
	IdPlayer = request.headers.get("id")
	RoomName = request.headers.get("roomname")
	mode = request.headers.get("mode")
	if IsNone(RoomName, IdPlayer):
		return request_error
	if mode == None:
		mode = "classic"
	return str(Rooms.CreateRoom(IdPlayer, RoomName, mode))

@app.route("/join", methods = ["GET", "POST"])
def JoinToRoom():
	IdPlayer = request.headers.get("id")
	RoomName = request.headers.get("roomname")
	if IsNone(RoomName, IdPlayer):
		return request_error
	return str(Rooms.JoinToRoom(IdPlayer, RoomName))

@app.route("/leave", methods = ["GET", "POST"])
def LeaveFromRoom():
	IdPlayer = request.headers.get("id")
	RoomName = request.headers.get("roomname")
	if IsNone(RoomName, IdPlayer):
		return request_error
	return str(Rooms.LeaveFromRoom(IdPlayer, RoomName))

Players = PlayersSave()
Rooms = RoomsClass()
app.run(host='0.0.0.0')