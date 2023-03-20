import traceback
def IsNone(*requests) -> bool:
	for i in requests:
		if i == None:
			return True
	return False
def NotHeaders(*headers):
	header = 0
	for elem in headers:
		if elem == None:
			return {"Error":header}
		header += 1
	return {"Ebat":1}
def Str2pos(pos:str) -> str:
	if pos == "null":
		raise KeyError("N/a")
	X = {"a":"0", "b":"1", "c":"2", "d":"3", "e":"4", "f":"5", "g":"6", "h":"7"}
	Y = {"0":"7", '1':"7", '2':"6", '3':"5", '4':"4", '5':"3", '6':"2", '7':"1", '8':"0"}
	x = {"0":"a", "1":"b", "2":"c", "3":"d", "4":"e", "5":"f", "6":"g", "7":"h"}
	y = {"7":"1", "6":"2", "5":"3", "4":"4", "3":"5", "2":"6", "1":"7", "0":"8"}
	try:
		return Y[pos[1]] + X[pos[0]]
	except KeyError:
		try:
			return x[pos[1]] + y[pos[0]]
		except KeyError:
			with open("Invalid.data", "a", encoding="utf-8") as file:
				file.write(f"Позиция - {pos}")
			print(traceback.format_exc())
			raise KeyError(f"Позиция - {pos} говно")
	#except TypeError:
	#	print("None? ", pos)
def PosConvertRev(pos:str):
	"e4 -> 44"
	poss = {"1":"a", "2":"b", "3":"c", "4":"d", "5":"e", "6":"f", "7":"g", "8":"h"}
	Result = "null"
	try:
		Result = f"{poss[pos[0]]}{pos[1]}"
	except:
		if pos[0] == "0" or pos[0] == 9:
			print("[Warring] Вы вышли за доску (это не проблема)")
		else:
			print("Неверные данные")
			print(traceback.format_exc())
	return Result
def PosConvert(pos:str) -> str:
	"e4 -> 54"
	poss = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
	Result = None
	try:
		Result = str(poss[pos[0]]) + pos[1]
	except:pass
	return Result
def ВсеДанныеИзСписка(Ключ:str, ИзСписка:dict) -> list:
	"""Это пиздец должен возващать в виде списка каждое значение ключей из комнат"""
	Список = ИзСписка
	ьуь = []
	for пиво in Список:
		"Процесс невозможен без пива"
		ьуь.append(пиво[Ключ])
	return ьуь
def ReverseBool(data:bool) -> bool:
	data = bool(data)
	if data:
		data = False
	else:
		data = True
	return data
if __name__ == "__main__":
	print(Str2pos("e2"))
	print(Str2pos("64"))
	"""
	[
			['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle'],
			['Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn'],
			['White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle']
		]
	"""
