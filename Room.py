import traceback
from Canvas import Canvas
from Player import PlayersSave
from threading import Thread
from time import sleep as НихуяНеДелать, time

from funcs import ReverseBool
Players = PlayersSave()
class RoomsClass:
	#[{"Name":str, "Players":[str, str], "MaxPlayers":str(int), "mode":{"free":False, "random":False, "fog":False}, "IsGameStarted":0,"WaitPlayer":0, "Canvas":...}]
	def __init__(self):
		self.RoomList = {"Rooms":[]}
	def CreateRoom(self, PlayerId:str, RoomName:str, mode:dict, Reversed:bool, MaxPlayers:int) -> str:
		global Players
		Nickname = ""
		for player in Players.Players:
			print(player, player["id"], PlayerId, player["nick"])
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
		self.RoomList["Rooms"].append({"Name":RoomName, "IsGameStarted":0, "Players":[], "MaxPlayers":int(MaxPlayers), "WaitPlayer":0, "mode":mode, "Reverse":int(Reversed), "Winner":-1, "Canvas":Canvas()})
		self.RoomList["Rooms"][-1]["Canvas"].CreateChessBoard(mode["random"])
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
	def UpdateWinner(self, RoomName):
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Leave":0, "description":"Room not detected"})
		Room["Winner"] = Room["Canvas"].getWinner()
		try:
			if Room["Winner"] != -1:
				if Room["Winner"] == 2:
					for player in Room["Players"]:
						Players.AddNotifications(player, {"type":"draw","description":f'Ничья в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
				else:
					Players.AddNotifications(Room["Players"][int(Room["Winner"])], {"type":"win","description":f'Победа в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
					Players.AddNotifications(Room["Players"][int(ReverseBool(int(Room["Winner"])))], {"type":"lose","description":f'Проигрыш в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
		except: print("Похуй")
	def LeaveFromRoom(self, PlayerId:str, RoomName:str):
		t = time()
		Gen = 0
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
		if len(Room["Players"]) == 0:
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		if Room["IsGameStarted"]:
			PlayerColor = self.RoomGetColor(RoomName, PlayerId)
			Room["Canvas"].Lose(int(PlayerColor[10] == "W"))
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		self.UpdateWinner(RoomName)
		try:
			Thread(target=self.jxfoep, args=(Room, Nickname)).run()
		except ValueError:
			return str({"Leave":0, "description":"Player not in room"})
		return str({"Leave":"1"})
	def RoomDelete(self, RoomName:str, *_):
		Thread(target=self.rd, args=(RoomName)).run()
	def rd(self, RoomName:str, *_):
		НихуяНеДелать(4)
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Leave":0, "description":"Room not detected"})
		self.RoomList["Rooms"].pop(self.RoomList["Rooms"].index(Room))
	def jxfoep(self, R, N, *_):
		Thread(target=self.odpzmg, args=(R, N)).run()
	def odpzmg(self, Room, Nickname):
		НихуяНеДелать(2)
		Room["Players"].pop(Room["Players"].index(Nickname))
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
		if Room["Players"][int(Room["WaitPlayer"])] != Nickname and Room["mode"]["free"] == False:
			return str({"Move":0, "description": f'{Room["Players"][Room["WaitPlayer"]]} ≠ {Nickname}'})
		try:
			PlayerColor = Room["Players"].index(Nickname)
		except:
			return str({"Move":0, "description":"The player is out of the room"})
		if not Room["IsGameStarted"]:
			return str({"Canvas":0, "description":"Game not started"})
		Mode = Room["mode"]
		result = Room["Canvas"].Move(startpos, endpos, PlayerColor, Mode, RoomName)
		if result == str({"Move":1}):
			if Room["WaitPlayer"]:
				Room["WaitPlayer"] = 0
			else:
				Room["WaitPlayer"] = 1
		elif result == str({"Move":2}):
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		self.UpdateWinner(RoomName)
		return result
	def show4mouse(self, RoomName, Color = None):
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return str({"Canvas":0, "description":"Room not detected"})
		if Room["mode"]["fog"] != "False":
			if Color == None:
				return str({"Canvas":0, "description":"FogWar been used, but color in request not been set"})
			return Room["Canvas"].WarFogGen(Color)
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