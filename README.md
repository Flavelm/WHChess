## Doc WHChess server

> Если есть 0, в return есть description:Error

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
    > {"id": int id}
### /register
  * headers
    * nick 
        > Login
    * pass 
        > Password
  * return
    * "{'PlayerRegistered': 0}"
      > ник занят
    * "{'PlayerRegistered': 1}"
      > ник не занят
### /create
  * headers
    * id
      > id игрока
    * RoomName
      > Имя комнаты
    * Режимы по умолчанию все режимы на False, это такие же header'ы
      * free
        > True or False, нет античита
      * random
        > True or False, рандомное расположение фигур на 1 и 8 линии
      * fog
        > True or False, туман войны
    * reverse
      > 0 or 1
    * maxplayers
      > int
  * return
    > "{'Create': 1}"
    > "{'Create': 0, 'description': 'Player not detected'}"
### /join
  * headers
    * id
      > id player
    * roomname
      > Имя комнаты
  * return
    > "{'Join': 0/1}"
### /leave
  * headers
    * id
      > id player
    * roomname
      > Имя комнаты
  * return
    > "{'Leave': 0/1}"
### /rooms
  * return
    > Список комнат в формате
      > 'Rooms': [{'Name': 'Fun', 'IsGameStarted': 0, 'Players': ['Nya'], 'MaxPlayers': 2, 'WaitPlayer': 0, 'mode': {'free': 'False', 'random': 'True', 'fog': 'True'}, 'Reverse': 0, 'Winner': -1}]
      > {...}
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
    > "{'Move': 1}"
    > "{'Move': 0}"
### /show
 * headers
   * roomname
   * color
     > Внимание! Можно не указывать если fog war выключен white или black, капс букв не учитывается
 * return
   > {'Canvas':['Black castle', 'Black knight', 'Black bishop', 'Black queen', 'Black king', 'Black bishop', 'Black knight', 'Black castle', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'Black pawn', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White pawn', 'White castle', 'White knight', 'White bishop', 'White queen', 'White king', 'White bishop', 'White knight', 'White castle'], "Winner":-1}
   * Winner
    > 1 белые; 0 чёрные; -1 игра ещё идёт
   > {"Canvas":0, "description":"Room not detected"}
### /show/common
  * headers
    * roomname
    * color
      > Внимание! Можно не указывать если fog war выключен white или black, капс букв не учитывается
  * return
    > {"Canvas":[[["Black knight", "Black king", "Black bishop", "Black queen", "Black castle", "Black castle", "Black knight", "Black bishop"], ["Black pawn", "Black pawn", "Black pawn", "Black pawn", "Black pawn", "Black pawn", "Black pawn", "Black pawn"], ["null", "null", "null", "null", "null", "null", "null", "null"], ["null", "null", "null", "null", "null", "null", "null", "null"], ["null", "null", "null", "null", "null", "null", "null", "null"], ["null", "null", "null", "null", "null", "null", "null", "null"], ["White pawn", "White pawn", "White pawn", "White pawn", "White pawn", "White pawn", "White pawn", "White pawn"], ["White castle", "White knight", "White castle", "White king", "White bishop", "White knight", "White queen", "White bishop"]]], "Winner":-1}
### /room
 * headers
   * roomname
 * return
   >  {'Name': 'Fun', 'IsGameStarted': 0, 'Players': ['Nya'], 'MaxPlayers': 2, 'WaitPlayer': 0, 'mode': {'free': 'False', 'random': 'True', 'fog': 'True'}, 'Reverse': 0, 'Winner': -1}
   >  {"Room":0, "description":"Room not detected"}
### /room/color
 * headers
   * id
     > Id игрока
   * roomname
 * return
  * {"Color":"White"} or {"Color":"Black"} or {"Color":0}(Error)
    > Более просто есть в room["Players"] но лучше этим пользоватся
### /notifications/player
 * headers
   * id
     > id игрока
 * return
  >  {'notifications': [{'type': 'server', 'description': 'Xyu'}]}
### /notifications/del_all
 * headers
   * id
     > id игрока
 * return
  > {"delete":0/1}
### /profile | /status
 * headers
   * id
     > id игрока
 * returns
   * {"Profile":0, "description":"Player not detected"}
   * {'Profile': {'win': 0, 'lose': -1, 'nick': 'lol', 'level': 0.75}}
### types notification
  * win
  * lose
  * draw
  * buy
  * server
  * promo
### /moves
  * headers
    * roomname
  * return
    * {"Moves": [ ["e2", "e4"], ["e7", "e5"], [".l.", ".l."] ]}
    * {"Moves":0, "description":"Room not detected"}
