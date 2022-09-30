from Canvas import Canvas
from Player import PlayersSave
from threading import Thread
Players = PlayersSave()
class RoomsClass:
	#{"Name":str, "Players":[str, str], "MaxPlayers":str(int), "IsGameStarted":False,"WaitPlayer":"0", "Canvas":...}0
	def __init__(self):
		self.RoomList = {"Rooms":[]}
	def CreateRoom(self, PlayerId:str, RoomName:str, mode:str) -> str:
		global Players
		Nickname = ""
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Create":"0", "description":"Player not detected"}) #"Player not detected"
		self.RoomList["Rooms"].append({"Name":RoomName, "IsGameStarted":0, "Players":[], "MaxPlayers":2, "WaitPlayer":0, "mode":"classic", "Canvas":Canvas()})
		self.RoomList["Rooms"][-1]["Canvas"].CreateChessBoard()
		Thread(target=self.JoinToRoom, args = (PlayerId, RoomName)).run()
		return {"Create":"1"}
	def JoinToRoom(self, PlayerId:str, RoomName:str) -> str:
		global Players
		Room = {}
		Nickname = ""
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Join":"0", "description":"Room not detected"})
		if len(Room["Players"]) == int(Room["MaxPlayers"]):
			return str({"Join":"0", "description":"Room is full"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Join":"0", "description":"Player not detected"})
		Room["Players"].append(Nickname)
		return str({"Join":"1"})
	def LeaveFromRoom(self, PlayerId:str, RoomName:str):
		global Players
		Nickname = ""
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Leave":"0", "description":"Room not detected"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Leave":"0", "description":"Player not detected"})
		Room["Players"].pop(Room["Players"].index(Nickname))
		return str({"Leave":"1"})
	def Move(self, startpos:str, endpos:str, RoomName:str, PlayerId:str) -> str:
		global Players
		Room = {}
		Nickname = ""
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Move":"0", "description":"Room not detected"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Move":"0", "description":"Player not detected"})
		if len(startpos) != 2 or len(endpos) != 2:
			return str({"Move":"0", "description":"Incorecteble position"})
		if Room["Players"][int(Room["WaitPlayer"])] != Nickname:
			return str({"Move":"0", "description": f'{Room["Players"][int(Room["WaitPlayer"])]} ≠ {Nickname}'})
		return Room["Canvas"].Move(startpos, endpos)
	def show4mouse(self, RoomName):
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Print":"0", "description":"Room not detected"})
		return Room["Canvas"].show4mouse(Room["Name"])
	def RoomsReturn(self):
		Info = self.RoomList["Rooms"]
		NewRoomList = []
		for Room in Info:
			NewRoom = {}
			for key in Room:
				if key != "Canvas":
					print(key, "\n", Room, "\n", NewRoom, "\n", type(key), type(Room))
					NewRoom[key] = Room[key]
			NewRoomList.append(NewRoom)
		return str({"Rooms":NewRoomList})
	def PrintCanvas(self, RoomName:str) -> str:
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Print":"0", "description":"Room not detected"})
		return Room["Canvas"].PrintChessBoard(Room["Name"])
	def __str__(self):
		return self.RoomList