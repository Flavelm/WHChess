import traceback
def IsNone(*requests) -> bool:
	for i in requests:
		if i == None:
			return True
	return False
def Str2pos(pos:str) -> str:
	X = {"a":"0", "b":"1", "c":"2", "d":"3", "e":"4", "f":"5", "g":"6", "h":"7"}
	Y = {'1':"7", '2':"6", '3':"5", '4':"4", '5':"3", '6':"2", '7':"1", '8':"0"}
	x = {"0":"a", "1":"b", "2":"c", "3":"d", "4":"e", "5":"f", "6":"g", "7":"h"}
	y = {"7":"1", "6":"2", "5":"3", "4":"4", "3":"5", "2":"6", "1":"7", "0":"8"}
	try:
		return Y[pos[1]] + X[pos[0]]
	except KeyError:
		try:
			return x[pos[1]] + y[pos[0]]
		except KeyError:
			print(traceback.format_exc())
			raise KeyError("Позиция - говно")
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
