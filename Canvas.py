from funcs import PosConvert, PosConvertRev, Str2pos
from random import shuffle
from copy import copy
from traceback import format_exc
class Canvas:
	def __init__(self):
		self.ChessBoard = []
		self.Winner = - 1
		self.CanKillOnWalk = False
	def CreateChessBoard(self, random = "False"):
		ChessBoard = [
			['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle'],
			['Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'],
			['White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn'],
			['White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle']
		]
		if random != "False":
			print("Перемешал")
			shuffle(ChessBoard[0])
			shuffle(ChessBoard[-1])
		self.ChessBoard = ChessBoard
	def WarFogGen(self, color:str) -> list:
		Field = []
		deltalist = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
		for y in range(8):
			temp = []
			for x in range(8):
				temp.append("fog")
			Field.append(temp)
		for y in range(8):
			for x in range(8):
				Element = self.ChessBoard[y][x]
				PieceType = Element[6:]
				PieceColor = Element[:5]
				if Element != "null" and color == PieceColor:
					Field[y][x] = Element
					for delta in deltalist:
						if x + delta[0] or y + delta[1] < 0: continue
						try: Field[y + delta[1]][x + delta[0]] = self.ChessBoard[y + delta[1]][x + delta[0]]
						except IndexError:continue
						except: print(format_exc())
					if PieceType == "pawn":
						for delta in [[0,2],[0,-2]]:
							if y + delta[1] < 0: continue
							try:
								Field[y + delta[1]][x + delta[0]] = self.ChessBoard[y + delta[1]][x + delta[0]]
							except IndexError:continue
							except: print(format_exc())
					if PieceType == "castle" or PieceType == "queen":
						for xp in range(1, 8):
							try:
								Field[y][x + xp] = self.ChessBoard[y][x + xp]
								if self.ChessBoard[y][x + xp] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for xm in range(1, 8):
							try:
								Field[y][x - xm] = self.ChessBoard[y][x - xm]
								if self.ChessBoard[y][x - xm] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for yp in range(1,8):
							if y + yp < 0: continue
							try:
								Field[y+yp][x] = self.ChessBoard[y+yp][x]
								if self.ChessBoard[y + yp][x] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for ym in range(1,8):
							if y - ym < 0: continue
							try:
								Field[y-ym][x] = self.ChessBoard[y-ym][x]
								if self.ChessBoard[y - ym][x] != "null":
									break
							except IndexError:break
							except: print(format_exc())
					if PieceType == "bishop" or PieceType == "queen":
						for xpyp in range(1,8):

							try:
								Field[y + xpyp][x + xpyp] = self.ChessBoard[y + xpyp][x + xpyp]
								if self.ChessBoard[y + xpyp][x + xpyp] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for xmym in range(1,8):
							if y - xmym < 0: continue
							try:
								Field[y - xmym][x - xmym] = self.ChessBoard[y - xmym][x - xmym]
								if self.ChessBoard[y - xmym][x - xmym] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for xpym in range(1,8):
							if y - xpym < 0: continue
							try:
								Field[y - xpym][x + xpym] = self.ChessBoard[y - xpym][x + xpym]
								if self.ChessBoard[y - xpym][x + xpym] != "null":
									break
							except IndexError:break
							except: print(format_exc())
						for xmyp in range(1,8):
							try:
								Field[y + xmyp][x - xmyp] = self.ChessBoard[y + xmyp][x - xmyp]
								if self.ChessBoard[y + xmyp][x - xmyp] != "null":
									break
							except IndexError:break
							except: print(format_exc())
					if PieceType == "knight":
						for delta in [ (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1), (2, 1), (2,-1) ]:
							if y + delta[1] < 0: continue
							try:   Field[y + delta[1]][x + delta[0]] = self.ChessBoard[y + delta[1]][x + delta[0]]
							except IndexError:continue
							except: print(format_exc())
		if __name__ == "__main__":
			return Field
		Pole = str(Field).replace("[","").replace("]","")
		return str("{'Canvas':[" + Pole + "], 'Winner':" + str(self.Winner) + "}")
	def Move(self, startpos:list, endpos:list, PlayerColor:bool, mode:str = "False", RoomName:str = "TestRoom"):
		if startpos == endpos:
			return str({"Move":0, "description":"StartPosition = EndPosition"})
		try:
			startpos = Str2pos(startpos)
			endpos = Str2pos(endpos)
			print("Debug poss", startpos, endpos)
		except KeyError:
			print("Некоректные данные")
			return str({"Move":0, "description":"PosError"})
		check_valide = mode != "True"
		SPosPiece = self.ChessBoard[int(startpos[0])][int(startpos[1])]
		EPosPiece = self.ChessBoard[int(endpos[0])][int(endpos[1])]
		Piece = SPosPiece[6:]
		if Piece == "king":
			print(endpos)
			if str(7 - 1) == endpos[1]:
				if self.ChessBoard[int(startpos[0])][int(startpos[1]) + 1] == "null" and self.ChessBoard[int(startpos[0])][int(startpos[1]) + 2] == "null" and self.ChessBoard[int(startpos[0])][int(startpos[1])+3][6:] == "castle":
					self.Replace(startpos, startpos[0]+str(int(startpos[1])+2))
					self.Replace(startpos[0]+str(int(startpos[1])+3),startpos[0]+str(int(startpos[1])+1))
					return str({"Move":1})
			elif str(3 - 1) == endpos[1]:
				if self.ChessBoard[int(startpos[0])][int(startpos[1]) - 1] == "null" and self.ChessBoard[int(startpos[0])][int(startpos[1]) + -2] == "null" and self.ChessBoard[int(startpos[0])][int(startpos[1]) + -3] == "null" and self.ChessBoard[int(startpos[0])][int(startpos[1])-4][6:] == "castle":
					self.Replace(startpos, startpos[0]+str(int(startpos[1])-2))
					self.Replace(startpos[0]+str(int(startpos[1])-4),startpos[0]+str(int(startpos[1])-1))
					return str({"Move":1})
		Color = SPosPiece[:5]
		EndPosColor = EPosPiece[:5]
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
			PlayerColor = 1
		else:
			PlayerColor = 0
		if bool(Color) != bool(PlayerColor) and check_valide:
			return str({"Move":0, "description":f"You don't have this piece {Piece} {bool(PlayerColor)} {Color}"})
		if SPosPiece == "null":
			return str({"Move":0, "description":"Piece is not found"})

		if not self.Valide(startpos, endpos, Piece, Color, EPosPiece, EndPosColor) and check_valide:
			return str({"Move":0, "description":"AntyCheat"})
		
		self.Replace(startpos, endpos)
		if  self.ChessBoard[int(startpos[0])][int(startpos[1])] != "null":
			self.ChessBoard[int(startpos[0])][int(startpos[1])] =  "null"
		
		if EPosPiece[6:] == "king":
			self.Win(Color)
		
		return str({"Move":1})
	def Replace(self, sp, ep):
		self.ChessBoard[int(sp[0])][int(sp[1])], self.ChessBoard[int(ep[0])][int(ep[1])] = self.ChessBoard[int(ep[0])][int(ep[1])], self.ChessBoard[int(sp[0])][int(sp[1])]
	def PrintChessBoard(self, RoomName):
		if self.ChessBoard == []:
			self.CreateChessBoard()
		Pole = str(self.WarFogGen("White"))
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
		Pole = Pole.replace("fog", "♀")
		pole = ""
		for symb in Pole:
			pole += symb + " "
		Pole = "Партия в комнате " + RoomName + "\n " + pole
		print(Pole)
		Pole = str(self.WarFogGen("Black"))
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
		Pole = Pole.replace("fog", "♀")
		pole = ""
		for symb in Pole:
			pole += symb + " "
		Pole = "Партия в комнате " + RoomName + "\n " + pole
		print(Pole)
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
		Pole = Pole.replace("fog", "♀")
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
	def draw(self):
		self.Winner = 2
	def Lose(self, loser:bool):
		if loser:
			self.Win(0)
		else:
			self.Win(1)
	def Нихуя(self):
		return "Рили нихуя"
	"""
	Piece = SPosPiece[6:]
	Color = SPosPiece[:5]
	"""
	def GetPieceFromField(self, pos:str) -> str:
		"human pos"
		try: pos = Str2pos(pos)
		except: pos = Str2pos(pos[1]+pos[0])
		cell = self.ChessBoard[int(pos[0])][int(pos[1])]
		return cell
	def KillPiece(self, poshum:str):
		pos = Str2pos(poshum)
		self.ChessBoard[int(pos[0])][int(pos[1])] = "null"
	def GenerateValideFields(self, PiecePosFromPosConvert:str, Piece:str, color:bool) -> list:
		self.CanKillOnWalk = False
		FieldList = []
		if color:
			ColorStr = "White"
		else:
			ColorStr = "Black"
		pos = PiecePosFromPosConvert
		pos = [int(pos[0]), int(pos[1])]
		for x in range(9):
			cache = []
			for y in range(9):
				cache.append(False)
			FieldList.append(cache)
		if Piece == "pawn":
			if pos[1] == 1 or pos[1] == 8:
				pass
			elif color:
				if pos[1] == 2:
					FieldList[pos[0]][pos[1]+1] = True
					FieldList[pos[0]][pos[1]+2] = True
				else:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]}{pos[1]+1}")) == "null":
						FieldList[pos[0]][pos[1]+1] = True
				print("Xyu", f"{pos[0]}{pos[1]}", PosConvertRev(f"{pos[0]+1}{pos[1]+1}"))
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]+1}{pos[1]+1}"))[:5] == "Black":
						FieldList[pos[0]+1][pos[1]+1] = True
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]-1}{pos[1]+1}"))[:5] == "Black":
						FieldList[pos[0]-1][pos[1]+1] = True
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]-1}{pos[1]}"))[6:] == "pawn" and int(pos[1]) == 4:
						FieldList[pos[0]-1][pos[1]+1] = True
						self.CanKillOnWalk = True
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]+1}{pos[1]}"))[6:] == "pawn" and int(pos[1]) == 4:
						FieldList[pos[0]+1][pos[1]+1] = True
						self.CanKillOnWalk = True
				except:pass
			else:
				if pos[1] == 7:
					FieldList[pos[0]][pos[1]-1] = True
					FieldList[pos[0]][pos[1]-2] = True
				else:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]}{pos[1]-1}")) != "null":#Вперёд
						FieldList[pos[0]][pos[1]-1] = True
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]+1}{pos[1]-1}"))[:5] == "White":
						FieldList[pos[0]+1][pos[1]-1] = True#Взятие
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]-1}{pos[1]-1}"))[:5] == "White":
						FieldList[pos[0]-1][pos[1]-1] = True
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]-1}{pos[1]}"))[6:] == "pawn" and int(pos[1]) == 5:
						FieldList[pos[0]-1][pos[1]+1] = True
						self.CanKillOnWalk = True
				except:pass
				try:
					if self.GetPieceFromField(PosConvertRev(f"{pos[0]+1}{pos[1]}"))[6:] == "pawn" and int(pos[1]) == 5:
						FieldList[pos[0]+1][pos[1]+1] = True
						self.CanKillOnWalk = True
				except:pass
		elif Piece == "castle":
			for yp in range(8):
				posx = pos[0]
				posy = pos[1] + yp + 1
				if posx > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for ym in range(8):
				posx = pos[0]
				posy = pos[1] - ym - 1
				if posx > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xp in range(8):
				posx = pos[0] + xp + 1
				posy = pos[1]
				if 1 >= posx >= 8:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xm in range(8):
				posx = pos[0] - xm - 1
				posy = pos[1]
				if 1 >= posx >= 8:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
		elif Piece == "queen":
			for yp in range(8):
				posx = pos[0]
				posy = pos[1] + yp + 1
				if posx > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for ym in range(8):
				posx = pos[0]
				posy = pos[1] - ym - 1
				if posx > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xp in range(8):
				posx = pos[0] + xp + 1
				posy = pos[1]
				if 1 >= posx >= 8:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xm in range(8):
				posx = pos[0] - xm - 1
				posy = pos[1]
				if posx > 0 and posx < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						print("TryPos = null")
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						print("Враг!")
						FieldList[posx][posy] = True
						break
					elif trypos[:5] != ColorStr:
						print("Друг!")
						break
				else:
					print(posx, "Многа", type(posx), posx > 0 and posx < 9, posx > 0, posx < 9)
					break
			for xyp in range(8):
				posx = pos[0] + xyp + 1
				posy = pos[1] + xyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xym in range(8):
				posx = pos[0] - xym - 1
				posy = pos[1] - xym	- 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xmyp in range(8):
				posx = pos[0] - xmyp - 1
				posy = pos[1] + xmyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xpym in range(8):
				posx = pos[0] + xpym + 1
				posy = pos[1] - xpym - 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
		elif Piece == "bishop":
			for xyp in range(8):
				posx = pos[0] + xyp + 1
				posy = pos[1] + xyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xym in range(8):
				posx = pos[0] - xym - 1
				posy = pos[1] - xym	- 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xmyp in range(8):
				posx = pos[0] - xmyp - 1
				posy = pos[1] + xmyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xpym in range(8):
				posx = pos[0] + xpym + 1
				posy = pos[1] - xpym - 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
		elif Piece == "king":
			for yp in range(1):
				posx = pos[0]
				posy = pos[1] + yp + 1
				if posx > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for ym in range(1):
				posx = pos[0]
				posy = pos[1] - ym - 1
				if posx > 0 and posy < 9:
					print(posx, posy)
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xp in range(1):
				posx = pos[0] + xp + 1
				posy = pos[1]
				if 1 >= posx >= 8:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xm in range(1):
				posx = pos[0] - xm - 1
				posy = pos[1]
				if posx > 0 and posx < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						print("TryPos = null")
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						print("Враг!")
						FieldList[posx][posy] = True
						break
					elif trypos[:5] != ColorStr:
						print("Друг!")
						break
				else:
					print(posx, "Многа", type(posx), posx > 0 and posx < 9, posx > 0, posx < 9)
					break
			for xyp in range(1):
				posx = pos[0] + xyp + 1
				posy = pos[1] + xyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xym in range(1):
				posx = pos[0] - xym - 1
				posy = pos[1] - xym	- 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xmyp in range(1):
				posx = pos[0] - xmyp - 1
				posy = pos[1] + xmyp + 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
			for xpym in range(1):
				posx = pos[0] + xpym + 1
				posy = pos[1] - xpym - 1
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						break
				else:
					break
		elif Piece == "knight":
			for NumPos in [ (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1), (2, 1), (2,-1) ]:
				posx = pos[0] + NumPos[0]
				posy = pos[1] + NumPos[1]
				if posx > 0 and posx < 9 and posy > 0 and posy < 9:
					trypos = self.GetPieceFromField(PosConvertRev(f"{posx}{posy}"))
					if trypos == "null":
						FieldList[posx][posy] = True
					elif trypos[:5] != ColorStr:
						FieldList[posx][posy] = True
						continue
				else:
					continue
		else:
			print("[Warring] Piece not use in AC")
			FieldList = []
			for x in range(9):
				cache = []
				for y in range(9):
					cache.append(True)
				FieldList.append(cache)
		return FieldList
	def CheatMove(self, startpos, endpos):
		self.ChessBoard[int(startpos[0])][int(startpos[1])], self.ChessBoard[int(endpos[0])][int(endpos[1])] = self.ChessBoard[int(endpos[0])][int(endpos[1])], self.ChessBoard[int(startpos[0])][int(startpos[1])]
		if  self.ChessBoard[int(startpos[0])][int(startpos[1])] != "null":
			self.ChessBoard[int(startpos[0])][int(startpos[1])] =  "null"
	def Valide(self, SPos:str, EPos:str, Piece:str, Color:bool, TargetPiece:str, TargetColor:bool) -> bool:
		SPos = Str2pos(SPos)
		if self.GetPieceFromField(SPos) == None:
			print("SPos = None")
			return False
		EPos = Str2pos(EPos)
		#Человеческий язык
		#e4
		pos0 = PosConvert(SPos)
		pos1 = PosConvert(EPos)
		print(SPos, EPos)
		if TargetColor == Color:
			print("TeamKill")
			return False
		TryMove = self.GenerateValideFields(pos0, Piece, Color)
		print(int(pos1[0]), int(pos1[1]))
		print("AC")
		if self.CanKillOnWalk and TryMove[int(pos1[0])][int(pos1[1])] and TargetPiece == "null":
			if Color:
				self.KillPiece(EPos[0]+str(int(EPos[1])-1))
			else:
				self.KillPiece(EPos[0]+str(int(EPos[1])+1))
			return True
		Result = TryMove[int(pos1[0])][int(pos1[1])]
		if not Result:
			print(TryMove)
		return Result
def test_ac(Posslist:str):
	Board = Canvas()
	Board.CreateChessBoard()
	GenList = Posslist
	GenList = GenList.replace(";", " ♂").replace(" /", "").split(" ♂ ")
	#['e2 e4 e7 e5', 'g1 f3 b8 c6', 'd2 d4 g8 f6', 'f3 d4 c6 d4', 'd1 d4 e4 c3', 'b1 c3 d7 d5', 'e5 d6 c7 d6', 'f1 b5 d8 d7', 'd4 e4 e8 d8', ' b5 d7  d8 d7', 'e1 g1 d6 d5', 'e4 d5 d7 c7', 'f1 e1 f8 d6', 'c3 b5 c7 b6', 'c1 e3 b5 d6 b6 a6', 'b5 d6 h8 d8', 'd5 b5']
	for element in GenList:
		print("Ход начинается, белые ходят" ,element[0:2], element[3:5], element[6:8], element[9:11], "\n")
		print(Board.Move(element[0:2], element[3:5], True))
		print("Чёрные ходят:")
		print(Board.Move(element[6:8], element[9:11], False))
		print("__________________________________________")
		Board.show4mouse("AC test")
if __name__ == "__main__":
	print("AC = antycheat")
	test_ac("e2 e4 / e7 e5")
	#test_ac("b2 b3 / e7 e5; e2 e4 / b8 c6; f1 c4 / g8 f6; d2 d3 / f8 b4; c1 d2 / b4 d2; b1 d2 / d7 d5; c4 b5 / a7 a6; b5 a4 / b7 b5; c2 c4 / b5 c4; a4 c6 / c8 d7; c6 a8 / d8 a8")
	#test_ac("e2 e4 / e7 e5; g1 f3 / d8 h4; f1 d3 / d7 d5; e1 g1 / c8 g4; f3 h4 / b8 a6; e4 d5 / e8 c8")