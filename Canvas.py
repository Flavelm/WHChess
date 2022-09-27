class Canvas:
	def __init__(self):
		self.ChessBoard = []
	def CreateChessBoard(self):
		self.ChessBoard = [
			['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle'],
			['Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn'],
			['White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle']
		]
		
		print(self.ChessBoard)
	def Move(self, startpos:list, endpos:list):
		X = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
		Y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
		try:
			startpos = Y[startpos[1]], X[startpos[0]]
			endpos = Y[endpos[1]], X[endpos[0]]
		except KeyError:
			print("Некоректные данные")
			print(traceback.format_exc())
			return str({"Move":"0", "description":"PosError"})
		SPosPiece = self.ChessBoard[startpos[0]][startpos[1]]
		EPosPiece = self.ChessBoard[endpos[0]][endpos[1]]
		if SPosPiece == "null":
			return str({"Move":"0", "description":"kill"})
		if self.ChessBoard[endpos[0]][endpos[1]] != "null":
			self.ChessBoard[endpos[0]][endpos[1]] = "null"
			print(2)
		self.ChessBoard[startpos[0]][startpos[1]], self.ChessBoard[endpos[0]][endpos[1]] = self.ChessBoard[endpos[0]][endpos[1]], self.ChessBoard[startpos[0]][startpos[1]]
		return str({"Move":"1"})
	def PrintChessBoard(self, RoomName):
		if self.ChessBoard == []:
			self.CreateChessBoard()
		Pole = str(self.ChessBoard)
		Pole = Pole.replace("'",'"')
		Pole = Pole.replace('"',"")
		Pole = Pole.replace(", ","")
		Pole = Pole.replace("],","\n")
		Pole = Pole.replace("[","")
		Pole = Pole.replace("]","\n")
		Pole = Pole.replace("White king","♚")
		Pole = Pole.replace("White queen", "♛")
		Pole = Pole.replace("Black king","♔")
		Pole = Pole.replace("Black queen", "♕")
		Pole = Pole.replace("White knight","♞")
		Pole = Pole.replace("Black knight", "♘")
		Pole = Pole.replace("White castle", "♜")
		Pole = Pole.replace("Black castle", "♖")
		Pole = Pole.replace("Black bishop", "♗")
		Pole = Pole.replace("White bishop", "♝")
		Pole = Pole.replace("White pawn", "♟")
		Pole = Pole.replace("Black pawn", "♙")
		Pole = Pole.replace("null", " ")
		pole = ""
		for symb in Pole:
			pole += symb + " "
		Pole = pole
		print("Партия в комнате " + RoomName)
		print(" " + Pole)
		return str(self.ChessBoard)
	def show4mouse(self, RoomName):
		self.PrintChessBoard(RoomName)
		Pole = str(self.ChessBoard).replace("[","").replace("]","")
		return str("{'Canvas':[" + Pole + "]}")
	def __str__(self):
		return str(self.ChessBoard)