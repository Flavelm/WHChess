## Doc WHChess server

> Если есть '0', в return есть description:Error

### /login
  * headers
    * nick 
        > Login
    * pass 
        > Password
    * platform(Platform + version game)
  * return id 
    * -2 bad nickname
    * -1 bad password
    * 10 000 and more --> complete
    > exemple
    > {"id":"int"}
### /register
  * headers
    * nick 
        > Login
    * pass 
        > Password
  * return
    * "{'PlayerRegistered': '0'}"
      > ник занят
    * "{'PlayerRegistered': '1'}"
      > ник не занят
### /create
  * headers
    * id
      > id игрока
    * RoomName
      > Имя комнаты
  * return
    * "{'Create': '1'}"
    * "{'Create': '0', 'description': 'Player not detected'}"
### /join
  * headers
    * id
      >id player
    * roomname
      >Имя комнаты
  * return
    > "{'Join': '0'/'1'}"
### /leave
  > Смотри join только не Join а Leave
### /rooms
  * return
    > Список комнат в формате
      > [{'Name': 'Fun', 'GameStarted': False, 'Players': ['Nya'], 'MaxPlayers': '2', 'WaitPlayer': '0', 'Canvas': <Canvas.Canvas object at 0x000001E8B97E7460>, 'mode': 'clasic'},
      > {...}]
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
  * return
    > "{'Move': '1'}"
    > "{'Move': '0'}"
### /show
 * headers
   * roomname
 * return
   > "{'Canvas':['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle'], "Winner":-1}"
     > 1 белые; 0 чёрные; -1 игра ещё идёт
### /room
 * headers
   * roomname
 * return
   > {"Name":RoomName, "IsGameStarted":0, "Players":[], "MaxPlayers":2, "WaitPlayer":0, "mode":"classic", "Reverse":int(Reversed), "Canvas":Canvas()}
### /room/color
 * headers
   * id
     > Id игрока
   * roomname
 * return
  * {"Color":"White"} or {"Color":"Black"} or {"Color":0}(Error)
    > Более просто есть в room["Players"] но лучше этим пользоватся
