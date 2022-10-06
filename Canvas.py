from funcs import Str2pos
class Canvas:
	def __init__(self):
		self.ChessBoard = []
		self.Winner = - 1
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
	def Move(self, startpos:list, endpos:list, PlayerColor:bool, mode:str, RoomName:str):
		if startpos == endpos:
			return str({"Move":0, "description":"StartPosition = EndPosition"})
		try:
			startpos = Str2pos(startpos)
			endpos = Str2pos(endpos)
		except KeyError:
			print("Некоректные данные")
			return str({"Move":0, "description":"PosError"})
		check_valide = mode == "classic"
		SPosPiece = self.ChessBoard[int(startpos[0])][int(startpos[1])]
		EPosPiece = self.ChessBoard[int(endpos[0])][int(endpos[1])]
		print(startpos, endpos)
		Piece = SPosPiece[6:]
		Color = SPosPiece[:5]
		EndPosPiece = EPosPiece[6:]
		EndPosColor = EPosPiece[:5]
		Kill  = False
		print("PosStart", SPosPiece, "End", EPosPiece, "\n", "Гавна", Piece, Color, EndPosPiece, EndPosColor)
		print(Color, "White", Color == "White")
		if Color == "White":
			Color = True
		elif Color == "Black":
			Color = False
		else:
			Color = None
		if  EndPosColor == "White":
			EndPosColor = True
		elif EndPosColor == "Black":
			EndPosColor = False
		else:
			EndPosColor = None
		if PlayerColor:
			PlayerColor = 0
		else:
			PlayerColor = 1
		print(bool(Color), bool(PlayerColor))
		if bool(Color) != bool(PlayerColor) and check_valide:
			return str({"Move":0, "description":"You don't have this piece"})
		print(Piece + "\n" + "Цвет " + str(Color))
		if SPosPiece == "null":
			return str({"Move":0, "description":"Piece is not found"})
		if self.ChessBoard[int(endpos[0])][int(endpos[1])] != "null":
			self.ChessBoard[int(endpos[0])][int(endpos[1])] = "null"
			Kill = True


			
		if not self.Valide(startpos, endpos, Piece, Color, EndPosPiece, EndPosColor, Kill) and check_valide:
			return str({"Move":0, "description":"AntyCheat"})



		self.ChessBoard[int(startpos[0])][int(startpos[1])], self.ChessBoard[int(endpos[0])][int(endpos[1])] = self.ChessBoard[int(endpos[0])][int(endpos[1])], self.ChessBoard[int(startpos[0])][int(startpos[1])]
		self.PrintChessBoard(RoomName)
		return str({"Move":1})
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
		Pole = Pole.replace("null", "♂")
		pole = ""
		
		for symb in Pole:
			pole += symb + " "
		Pole = "Партия в комнате " + RoomName + "\n " + pole
		print(Pole)
	def getWinner(self):
		return self.Winner
	def show4mouse(self, RoomName):
		self.PrintChessBoard(RoomName)
		Pole = str(self.ChessBoard).replace("[","").replace("]","")
		return str("{'Canvas':[" + Pole + "], 'Winner':" + str(self.Winner) + "}")
	def Win(self, winner:bool):
		self.Winner = int(winner)
	def Lose(self, loser:bool):
		if loser:
			self.Win(0)
		else:
			self.Win(1)
	def Нихуя(self):
		return "Рили нихуя"
	def Valide(self, SPos:str, EPos:str, Piece:str, Color:bool, TargetPiece:str, TargetColor:bool, Kill:bool) -> bool:
		SPos = Str2pos(SPos)
		EPos = Str2pos(EPos)
		#Человеческий язык
		#e4
		print(SPos, EPos)
		if TargetColor == Color:
			print("TeamKill")
			return False
		if Piece == "pawn":
			if Color:
				if int(SPos[1]) == 2:
					if int(EPos[1]) == 3 or int(EPos[1]) == 4:
						print("Белая логика wp")
						return True
					else:
						print(EPos[1])
						return False
			else:
				if int(SPos[1]) == 7:
					print("Чёрная логика")
					if int(EPos[1]) == 6 or int(EPos[1]) == 5:
						return True
					else:
						return False
		return True
if __name__ == "__main__":
	Board = Canvas()
	Board.CreateChessBoard()
	Board.show4mouse("test")
	print(Board.Move("e2", "e4", True))
	Board.PrintChessBoard("Fuck")
	print(Board.Move("e7", "e5", False))
	Board.PrintChessBoard("Fuck")
	print(Board.Move("e4", "e5", True))
	Board.PrintChessBoard("Fuck")
	print(Board.Move("d7", "d5", False))
	Board.PrintChessBoard("koef")
	print(Board.Move("d2", "d4", True))
	Board.PrintChessBoard("edrg")
	print(Board.Move("d8", "h4", False))
	Board.PrintChessBoard("z")
	print(Board.Move("d1", "h5", True))
	Board.PrintChessBoard("Z")
	print(Str2pos("32"))
	Board.PrintChessBoard("SSD")