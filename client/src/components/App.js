import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Game from "./Game";
import Homepage from "./Homepage";
import io from "socket.io-client";

function App() {
  
  const [gameData, setGameData] = useState({})
  const socket = io("http://localhost:5555");

  function fillGameData(user, code) {
    const data = {"user": user, "room": code}
    setGameData(data);
  }

  return (
  <div>
    <Switch>
      <Route path="/game">
        <Game gameData={gameData} socket={socket}/>
      </Route>
      <Route path="/">
        <Homepage fillGameData={fillGameData}/>
      </Route> 
    </Switch>
  </div>
  )
}

export default App;
