## Doc WHChess server

> Всё то что было выполнено удачно return "0"

### /login
  * headers
    * nick 
        > Login
    * pass 
        > Password
    * Client(Platform + version game)
  * return id 
    * -2 bad nickname
    * -1 bad password
    * 10 000 and more --> complete
### /register
  * headers
    * nick 
        > Login
    * pass 
        > Password
  * return
    * "1"
      > ник занят
    * id игрока
      > ник не занят
### /create
  * headers
    * id
      > id игрока
    * RoomName
      > Имя комнаты
  * return
    * "0"
    * "Error"
### /join
  * headers
    * id
      >id player
    * roomname
      >Имя комнаты
  * return
    > "0" or error
### /leave
  > Смотри join
### /rooms
  * return
    > Список комнат в формате
      > [{"Name":str, "Players":[str, str], "MaxPlayers":str(int), "GameStarted":False,"WaitPlayer":"0", "canvas":...},
      > {"Name":str, "Players":[str, str], "MaxPlayers":str(int), "GameStarted":False,"WaitPlayer":"0", "canvas":...},
      > {"Name":str, "Players":[str, str], "MaxPlayers":str(int), "GameStarted":False,"WaitPlayer":"0", "canvas":...}]
### /move
  * headers
    * startpos
      > e2
    * endpos
      > e4
    * roomname
      > Имя комнаты
    * id
      > Имя игрока
### /show
 * headers
  * roomname
    >Имя комнаты
 * return
  > Игровое поле
  > exemple:
  > "[['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle'], ['Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn'], ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'], ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'], ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'], ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'], ['White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn'], ['White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle']]"
