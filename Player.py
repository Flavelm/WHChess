import json
from random import randint
class PlayersSave:
	Players = []
	#{"nick": str, "pass": str, "id": int, "money": 0, "platforms": [], "items":["ClassicBoard", "ClassicPiece"], "UseDefault":{"ColorChessBoard":"ClassicBoard", "ColorChessPiece":"ClassicPiece"}}
	def __init__(self):
		self.Players = []
		self.load()
	def load(self):
		try:
			with open("PlayersSave.json", "r", encoding = "utf-8") as PlayerSaveFile:
				self.Players = json.load(PlayerSaveFile)
		except OSError:
			with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
				json.dump(self.Players, PlayerSaveFile)
	def write(self):
		with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
			json.dump(self.Players, PlayerSaveFile)
	def __str__(self):
		return self.Players
	def login(self, nickname:str, password:str, platform:str):
		self.load()
		id = -2
		for player in self.Players:
			if str(player["nick"]) == nickname:
				id = -1
				if player["pass"] == password:
					id = player["id"]
					id = int(id)
					if platform in player["platforms"]:
						player["platforms"].pop(player["platforms"].index(platform))
					player["platforms"].append(platform)
					self.write()
					return str({"id": id})
				else:
					return str({"id": id})
		return str({"id": id})

	def register(self, nickname:str, password:str):
		self.load()
		for Player in self.Players:
			if Player["nick"] == nickname:
				return str({"PlayerRegistered":0, "description":"Игрок с таким ником уже зарегистрирован"})
		id = 0
		while id == 0:
			id = randint(10000, 999999999999999999)
			for player in self.Players:
				if player["id"] == id:
					id = 0
					break
		self.Players.append({"nick": nickname, "pass": password, "id": str(id), "money":0, "platforms":[], "items":["ClassicBoard", "ClassicPiece"], "UseDefault":{"ColorChessBoard":"ClassicBoard", "ColorChessPiece":"ClassicPiece", "notifications":[]}})
		self.write()
		return str({"PlayerRegistered":1})

	def GetNotification(self, PlayerId) -> dict:
		self.load()
		Nickname = ""
		for player in self.Players:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return str({"Notifications":0, "description":"Player not detected"})
		for player in self.Players:
			if player["nick"] == Nickname:
				return str({"notifications":player["notifications"]})
	def AddNotifications(self, nickname:str, data:dict) -> int:
		"""
		data = {"type":"win" or "lose" or "draw" or "buy" or "server" or "promo", "description":str}
		"""
		self.load()
		for player in self.Players:
			if str(player["nick"]) == nickname:
				if player["notifications"] == [] or player["notifications"][-1] != data:
					player["notifications"].append(data)
					self.write()
		return "llUBO"