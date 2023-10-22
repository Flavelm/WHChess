import json
from random import randint
class PlayersSave:
	Player = []
	#{"nick": str, "pass": str, "id": str, "platforms": [], "notifications":[], "profile":{"win":int, "lose":int, "all":int "nick":str, "level":float}}
	def __init__(self):
		self.Player = []
		self.load()
	def Players(self):
		self.load()
		return self.Player
	def load(self):
		try:
			with open("PlayersSave.json", "r", encoding = "utf-8") as PlayerSaveFile:
				self.Player = json.load(PlayerSaveFile)
		except OSError:
			with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
				json.dump(self.Player, PlayerSaveFile)
	def write(self):
		with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
			json.dump(self.Player, PlayerSaveFile)
	def __str__(self):
		return self.Player
	def login(self, nickname:str, password:str, platform:str):
		self.load()
		id = -2
		for player in self.Player:
			if str(player["nick"]) == nickname:
				id = -1
				if player["pass"] == password:
					id = player["id"]
					id = int(id)
					if platform in player["platforms"]:
						player["platforms"].pop(player["platforms"].index(platform))
					player["platforms"].append(platform)
					self.write()
					return {"id": id}
				else:
					return {"id": id}
		return {"id": id}

	def register(self, nickname:str, password:str):
		if not 2 < len(nickname) < 20:
			return {"PlayerRegistered":0, "description":"long or short nick"}
		BadNicks = "xyu anal fuck mouse blyat 4mo The_EnG1nE qwerty".split(" ")
		for Nicks in BadNicks:
			if Nicks in nickname:
				return {"PlayerRegistered":0, "description":"bad nick"}
		if " " in nickname:
			return {"PlayerRegistered":0, "description":"space in nickname"}
		self.load()
		for Player in self.Player:
			if Player["nick"] == nickname:
				return {"PlayerRegistered":0, "description":"Player with your nick been created"}
		id = 0
		while id == 0:
			id = randint(10000, 2147483647)
			for player in self.Player:
				if player["id"] == id:
					id = 0
					break
		self.Player.append({"nick": nickname, "pass": password, "id": str(id), "money":0, "platforms":[], "notifications":[], "profile":{"win":0, "lose":0, "nick":nickname,"level":1.0}})#"nick": str, "pass": str, "id": str, "platforms": [], "notifications":[], "profile":{"win":int, "lose":int, "nick":str, "level":float
		self.write()
		return {"PlayerRegistered":1}

	def GetNotification(self, PlayerId) -> dict:
		self.load()
		Nickname = ""
		for player in self.Player:
			if player["id"] == PlayerId:
				Nickname = player["nick"]
		if Nickname == "":
			return {"Notifications":0, "description":"Player not detected"}
		for player in self.Player:
			if player["nick"] == Nickname:
				return {"notifications":player["notifications"]}
	def AddNotifications(self, nickname:str, data:dict) -> int:
		"""
		data = {"type":"win" or "lose" or "draw" or "buy" or "server" or "promo", "description":str}
		"""
		self.load()
		for player in self.Player:
			if str(player["nick"]) == nickname:
				if player["notifications"] == [] or player["notifications"][-1] != data:
					st = player["profile"]
					if data["type"] == "win":
						st["win"]+=1
						st["level"] += .5 / st["level"]
					elif data["type"] == "lose":
						st["lose"]+=1
						st["level"] -= (.5 / st["level"]) / 2
					st["level"] = round(st["level"],2)
					print(nickname, st["level"])
					player["notifications"].append(data)
					self.write()
		return "llUBO"
	def DelAllNotification(self, PlayerId:str):
		self.load()
		for player in self.Player:
			if player["id"] == PlayerId:
				player["notifications"] = []
				self.write()
				return '{"delete":1}'
		return '{"delete":0}'
	def GetProfile(self, id):
		profile = ""
		for player in self.Players():
			if player["id"] == id:
				profile = {"Profile":player["profile"]}
				print(profile)
		if profile == "":
			return {"Profile":0, "description":"Player not detected"}
		return profile