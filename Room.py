import traceback
from Canvas import Canvas
from Player import PlayersSave
from threading import Thread
from time import sleep as НихуяНеДелать
Players = PlayersSave()
class RoomsClass:
	#[{"Name":str, "Players":[str, str], "MaxPlayers":str(int), "IsGameStarted":0,"WaitPlayer":0, "Canvas":...}]
	def __init__(self):
		self.RoomList = {"Rooms":[]}
	def CreateRoom(self, PlayerId:str, RoomName:str, mode:str, Reversed:bool, MaxPlayers:int) -> str:
		global Players
		Nickname = ""
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Create":0, "description":"Player not detected"}) #"Player not detected"
		if RoomName in self.СтрашнаяПиздотня("Name"):
			return str({"Create":0, "description":'Room with name "' + RoomName + '" been created'})
		for Player1 in self.СтрашнаяПиздотня("Players"):
			for Player in Player1:
				if Nickname == Player:
					return str({"Create":0, "description":"Player in room"})
		self.RoomList["Rooms"].append({"Name":RoomName, "IsGameStarted":0, "Players":[], "MaxPlayers":int(MaxPlayers), "WaitPlayer":0, "mode":str(mode), "Reverse":int(Reversed), "Winner":-1, "Canvas":Canvas()})
		self.RoomList["Rooms"][-1]["Canvas"].CreateChessBoard()
		Thread(target=self.JoinToRoom, args = (PlayerId, RoomName)).run()
		return {"Create":1}
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
			return str({"Join":0, "description":"Room not detected"})
		if len(Room["Players"]) == int(Room["MaxPlayers"]):
			return str({"Join":0, "description":"Room is full"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Join":0, "description":"Player not detected"})
		for Player1 in self.СтрашнаяПиздотня("Players"):
			for Player in Player1:
				if Nickname == Player:
					return str({"Join":0, "description":"Player in room"})
		Room["Players"].append(Nickname)
		if len(Room["Players"]) == 2:
			Room["IsGameStarted"] = 1
			if bool(Room["Reverse"]):
				Room["Players"].reverse()
				print("Создатель играет за чёрных")
			else:
				print("Создатель играет за белых")
		return str({"Join":"1"})
	def UpdateWinner(self):
		self.RoomList["Winner"] = self.RoomList["Canvas"].getWinner()
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
			return str({"Leave":0, "description":"Room not detected"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Leave":0, "description":"Player not detected"})
		try:
			Room["Players"].pop(Room["Players"].index(Nickname))
		except ValueError:
			return str({"Leave":0, "description":"Player not in room"})
		if len(Room["Players"]) == 0:
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		if Room["IsGameStarted"]:
			PlayerColor = self.RoomGetColor(RoomName, PlayerId)
			if PlayerColor[10] == "W":
				PlayerColor = 1
			else:
				PlayerColor = 0
			Room["Canvas"].Lose(PlayerColor)
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		self.UpdateWinner()
		return str({"Leave":"1"})
	def RoomDelete(self, RoomName:str):
		НихуяНеДелать(60)
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Leave":0, "description":"Room not detected"})
		self.RoomList["Rooms"].pop(self.RoomList["Rooms"].index(Room))
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
			return str({"Move":0, "description":"Room not detected"})
		if not Room["IsGameStarted"]:
			return str({"Move":0, "description":"Game not started"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Move":0, "description":"Player not detected"})
		if len(startpos) != 2 or len(endpos) != 2:
			return str({"Move":0, "description":"Incorecteble position"})
		if Room["Players"][int(Room["WaitPlayer"])] != Nickname:
			return str({"Move":0, "description": f'{Room["Players"][Room["WaitPlayer"]]} ≠ {Nickname}'})
		try:
			PlayerColor = Room["Players"].index(Nickname)
		except:
			return str({"Move":0, "description":"The player is out of the room"})
		if not Room["IsGameStarted"]:
			return str({"Canvas":0, "description":"Game not started"})
		Mode = Room["mode"]
		if Mode == "classic" or Mode == "free":
			Mode = Room["mode"]
		result = Room["Canvas"].Move(startpos, endpos, PlayerColor, Mode, RoomName)
		if result == str({"Move":1}):
			if Room["WaitPlayer"]:
				Room["WaitPlayer"] = 0
			else:
				Room["WaitPlayer"] = 1
		elif result == str({"Move":2}):
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		self.UpdateWinner()
		return result
	def show4mouse(self, RoomName):
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Canvas":0, "description":"Room not detected"})
		return Room["Canvas"].show4mouse(Room["Name"])
	def RoomsReturn(self):
		Info = self.RoomList["Rooms"]
		NewRoomList = []
		for Room in Info:
			NewRoom = {}
			for key in Room:
				if key != "Canvas":
					NewRoom[key] = Room[key]
			NewRoomList.append(NewRoom)
		return str({"Rooms":NewRoomList})
	def RoomGetColor(self, RoomName, PlayerId) -> str:
		global Players
		Room = {}
		Nickname = ""
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Color":0, "description":"Room not detected"})
		for player in Players.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Color":0, "description":"Player not detected"})
		if len(Room["Players"]) != Room["MaxPlayers"]:
			return str({"Color":0, "description":"Room not full"})
		if Room["Players"][0] == Nickname or Room["Players"][1] == Nickname:
			if Room["Players"].index(Nickname):
				return str({"Color":"Black"})
			return str({"Color":"White"})
		return str({"Color":0, "description":"Player not in room"})
	
	def СтрашнаяПиздотня(Экземпляр, Ключ:str) -> list:
		"""Это пиздец должен возващать в виде списка каждое значение ключей из комнат"""
		ВсеКомнаты = Экземпляр.RoomList["Rooms"]
		ьуь = []
		for пиво in ВсеКомнаты:
			"Процесс невозможен без пива"
			ьуь.append(пиво[Ключ])
		return ьуь
	def RoomReturn(self, RoomName:str) -> str():
		#[{"Name":str, "Players":[str, str], "MaxPlayers":str(int), "IsGameStarted":False,"WaitPlayer":0, "Canvas":...}]
		Room = {}
		try:
			for i in self.RoomList["Rooms"]:
				if i["Name"] == RoomName:
					Room = i
					break
		except:
			print(traceback.format_exc())
			return str({"Room":0, "description":"Room not detected"})
		if Room == {}:
			return str({"Room":0, "description":"Room not detected"})
		NewRoom = {}
		for key in Room:
			if key != "Canvas":
				NewRoom[key] = Room[key]
		return str(NewRoom)
	def PrintCanvas(self, RoomName:str) -> str:
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Canvas":0, "description":"Room not detected"})
		return Room["Canvas"].PrintChessBoard(Room["Name"])
	def __str__(self):
		return self.RoomList