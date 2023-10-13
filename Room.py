import traceback
from Canvas import Canvas
from Player import PlayersSave
from threading import Thread
from time import sleep as НихуяНеДелать, time
import json
from funcs import ReverseBool
Players = PlayersSave()
class RoomsClass:
	#[{"Name":str, "Players":[str, str], "Chat":[], "MaxPlayers":str(int), "mode":{"free":False, "random":False, "fog":False}, "IsGameStarted":0,"WaitPlayer":0, "Canvas":...}]
	def __init__(self):
		self.RoomList = {"Rooms":[]}
	def CreateRoom(self, PlayerId:str, RoomName:str, mode:dict, Reversed:bool, MaxPlayers:int) -> str:
		if " " in RoomName:
			return {"Create":0, "description":"space in room name"}
		global Players
		Nickname = ""
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Create":0, "description":"Player not detected"} #"Player not detected"
		if RoomName in self.СтрашнаяПиздотня("Name"):
			return {"Create":0, "description":'Room with name "' + RoomName + '" been created'}
		for Player1 in self.СтрашнаяПиздотня("Players"):
			for Player in Player1:
				if Nickname == Player:
					return {"Create":0, "description":"Player in room"}
		self.RoomList["Rooms"].append({"Name":RoomName, "IsGameStarted":0, "Players":[], "Chat":[], "MaxPlayers":int(MaxPlayers), "WaitPlayer":0, "mode":mode, "Reverse":Reversed, "Winner":-1, "Canvas":Canvas()})
		print("mods -", mode)
		self.RoomList["Rooms"][-1]["Canvas"].CreateChessBoard(bool(mode["random"]))
		Thread(target=self.JoinToRoom, args = (PlayerId, RoomName)).run()
		return {"Create":1}
	def GetHistory(self, RoomName):
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Moves":0, "description":"Room not detected"}
		return str({"Moves":Room["Canvas"].GetHistory})
	def GetChat(self, RoomName:str):
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"ChatHistory":0, "description":"Room not detected"}
		return {"ChatHistory":Room["Chat"]}
	def SendMessage(self, Message:str, PlayerId:str, RoomName:str):
		global Players
		Nickname = ""
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"SendMessage":0, "description":"Room not detected"}
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"SendMessage":0, "description":"Player not detected"}
		Room["Chat"].append(f"{Nickname}: {Message}")
		return {"SendMessage":1}
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
			return {"Join":0, "description":"Room not detected"}
		if len(Room["Players"]) == int(Room["MaxPlayers"]):
			return {"Join":0, "description":"Room is full"}
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Join":0, "description":"Player not detected"}
		for Player1 in self.СтрашнаяПиздотня("Players"):
			for Player in Player1:
				if Nickname == Player:
					return {"Join":0, "description":"Player in room"}
		Room["Players"].append(Nickname)
		if len(Room["Players"]) == int(Room["MaxPlayers"]):
			Room["IsGameStarted"] = 1
			if not bool(Room["Reverse"]):
				print("Создатель играет за белых")
			else:
				Room["Players"].reverse()
				print("Создатель играет за чёрных")
		return {"Join":"1"}
	def UpdateWinner(self, RoomName):
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Leave":0, "description":"Room not detected"}
		Room["Winner"] = Room["Canvas"].getWinner()
		try:
			if Room["Winner"] != -1:
				if Room["Winner"] == 2:
					for player in Room["Players"]:
						Players.AddNotifications(player, {"type":"draw","description":f'Ничья в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
				else:
					Players.AddNotifications(Room["Players"][int(Room["Winner"])], {"type":"win","description":f'Победа в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
					Players.AddNotifications(Room["Players"][int(ReverseBool(int(Room["Winner"])))], {"type":"lose","description":f'Проигрыш в комнате {RoomName}, партия между {Room["Players"][0]} и {Room["Players"][1]}'})
		except: print("Похуй", traceback.format_exc())
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
			return {"Leave":0, "description":"Room not detected"}
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Leave":0, "description":"Player not detected"}
		if Room["IsGameStarted"]:
			Room["Canvas"].Lose(int(json.loads(str(self.RoomGetColor(RoomName, PlayerId)).replace("'", "\""))["Color"] == "White"))
			self.UpdateWinner(RoomName)
		try:
			self.jxfoep(Room, Nickname)
		except ValueError:
			return {"Leave":0, "description":"Player not in room"}
		if Room["IsGameStarted"]:
			self.RoomDelete(RoomName)
		if len(Room["Players"]) == 0:
			self.RoomDelete(RoomName)
		return {"Leave":1}
	def RoomDelete(self, RoomName:str, *_):
		print(RoomName)
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			if MyRoom["Name"] == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Leave":0, "description":"Room not detected"}
		self.RoomList["Rooms"].pop(self.RoomList["Rooms"].index(Room))
	def jxfoep(self, Room, Nickname, *_):
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
			return {"Move":0, "description":"Room not detected"}
		if not Room["IsGameStarted"]:
			return {"Move":0, "description":"Game not started"}
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Move":0, "description":"Player not detected"}
		if len(startpos) != 2 or len(endpos) != 2:
			return {"Move":0, "description":"Incorecteble position"}
		if not Room["mode"]["free"]:
			if Room["Players"][int(Room["WaitPlayer"])] != Nickname:
				return {"Move":0, "description": f'{Room["Players"][Room["WaitPlayer"]]} ≠ {Nickname}'}
		try: PlayerColor = int(Room["Players"].index(Nickname) % 2 == 0)
		except: return {"Move":0, "description":"The player is out of the room"}
		if not Room["IsGameStarted"]:
			return {"Move":0, "description":"Game not started"}
		Mode = Room["mode"]
		result = Room["Canvas"].Move(startpos, endpos, PlayerColor, Mode)
		if result == str({"Move":1}):
			if Room["MaxPlayers"] == 1 or Room["WaitPlayer"] + 1 > Room["MaxPlayers"]:
				Room["WaitPlayer"] = 0
			else:
				Room["WaitPlayer"] += 1
		elif result == str({"Move":2}):
			Thread(target = self.RoomDelete, args = (RoomName)).run()
		self.UpdateWinner(RoomName)
		return result
	def showcommon(self, RoomName, id):
		global Players
		Room = {}
		Nickname = ""
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Canvas":0, "description":"Room not detected"}
		if Room["mode"]["fog"] != "False":
			for player in Players.Players():
				if player["id"] == id:
					Nickname = player["nick"]
			if Nickname == "":
				return {"Canvas":0, "description":"Player not detected"}
			Color = bool(Room["Players"].index(Nickname))
			if Color == None:
				return {"Canvas":0, "description":"FogWar been used, but id in request not been set"}
			return Room["Canvas"].CommonShow(Room["Name"], Room["mode"]["fog"], Color)
		return     Room["Canvas"].CommonShow(Room["Name"])
	def show4mouse(self, RoomName, id):
		global Players
		Room = {}
		Nickname = ""
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Canvas":0, "description":"Room not detected"}
		if Room["mode"]["fog"] != "False":
			for player in Players.Players():
				if player["id"] == id:
					Nickname = player["nick"]
			if Nickname == "":
				return {"Canvas":0, "description":"Player not detected"}
			Color = bool(Room["Players"].index(Nickname))
			if Color == None:
				return {"Canvas":0, "description":"FogWar been used, but id in request not been set"}
			return Room["Canvas"].show4mouse(Room["Name"], Room["mode"]["fog"], Color)
		return     Room["Canvas"].show4mouse(Room["Name"])
	def RoomsReturn(self) -> dict:
		Info = self.RoomList["Rooms"]
		NewRoomList = []
		for Room in Info:
			NewRoom = {}
			for key in Room:
				if key != "Canvas":
					NewRoom[key] = Room[key]
			Room["Reverse"] = int(Room["Reverse"])
			NewRoomList.append(NewRoom)
		return {"Rooms":NewRoomList}
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
			return {"Color":0, "description":"Room not detected"}
		for player in Players.Players():
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Color":0, "description":"Player not detected"}
		if len(Room["Players"]) != Room["MaxPlayers"]:
			return {"Color":0, "description":"Room not full"}
		if Room["Players"][0] == Nickname or Room["Players"][1] == Nickname:
			if Room["Players"].index(Nickname):
				return {"Color":"Black"}
			return {"Color":"White"}
		return {"Color":0, "description":"Player not in room"}
	
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
			return {"Room":0, "description":"Room not detected"}
		if Room == {}:
			return {"Room":0, "description":"Room not detected"}
		NewRoom = {}
		for key in Room:
			if key != "Canvas":
				NewRoom[key] = Room[key]
		NewRoom["Reverse"] = int(bool(NewRoom["Reverse"]))
		return NewRoom
	def PrintCanvas(self, RoomName:str) -> str:
		global Players
		Room = {}
		for MyRoom in self.RoomList["Rooms"]:
			NameRoom = MyRoom["Name"]
			if NameRoom == RoomName:
				Room = MyRoom
				break
		if Room == {}:
			return {"Canvas":0, "description":"Room not detected"}
		return Room["Canvas"].PrintChessBoard(Room["Name"])
	def __str__(self):
		return self.RoomList