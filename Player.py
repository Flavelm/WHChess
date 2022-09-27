import json, os
class PlayersSave:
	Players = []
	#{"nick":"Nya", "pass":"Me0w", "id":"0", "money":"0"}
	def __init__(self):
		self.load()
	def load(self):
		try:
			with open("PlayersSave.json", "r", encoding = "utf-8") as PlayerSaveFile:
				self.Players = json.load(PlayerSaveFile)
		except OSError:
			with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
				json.dump(self.Players, PlayerSaveFile)
			print("Файл не был найеден, я создал новый")
		print(self.Players)
	def write(self):
		print("Сохранение ♂♀♂")
		with open("PlayersSave.json", "w", encoding = "utf-8") as PlayerSaveFile:
			json.dump(self.Players, PlayerSaveFile)
		print("Файл был сохранён")
	def __str__(self):
		return self.Players
	def login(self, nickname:str, password:str, platform:str):
		id = -2
		print(self.Players)
		for player in self.Players:
			print(player)
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
		for Player in self.Players:
			if Player["nick"] == nickname:
				return str({"PlayerRegistered":"0"}) #"Игрок с таким ником уже зарегистрирован"
		id = 0
		while id == 0:
			id = randint(10000, 999999999999999999)
			for player in self.Players:
				player["id"] == id
				id = 0
				print("Случилось невероятное")
				break
		self.write()
		return str({"PlayerRegistered":"1"})
