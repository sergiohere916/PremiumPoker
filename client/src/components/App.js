import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Game from "./Game";
import Homepage from "./Homepage";
import io from "socket.io-client";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Login from "./Login"
import Signup from "./Signup";


const socket = io("http://localhost:5555");
function App() {
  
  const [gameData, setGameData] = useState({})
  const history = useHistory()
  
  //If idea does not work must return socket={socket} to Game component
  function fillGameData(user, code, userId) {
    const data = {"user": user, "room": code, "userId": userId }
    fetch("/storeData", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    })
    .then(r => {
      if (r.ok) {
        r.json()
        .then(confirmedData => {
          setGameData(confirmedData)
          history.push("/game")
        })
      } else {
        alert("failed to store data for game")
      }
    })
    // setGameData(data);
  }


  function restoreGameData(user, code, userId) {
    setGameData({"user": user, "room": code, "userId": userId})
  }

  useEffect(() => {
    fetch("/icons")
    .then(response => response.json())
    .then(data => {
      console.log(data)
    })
  }, [])

  
  return (
  <div id="page">
    <Switch>
      <Route path="/game">
        <Game gameData={gameData} socket={socket} restoreGameData={restoreGameData}/>
      </Route>
      <Route exact path="/">
        <Homepage fillGameData={fillGameData}/>
      </Route> 
      <Route exact path="/login">
        <Login></Login>
      </Route>
      <Route exact path="/signup">
        <Signup></Signup>
      </Route>
      <Route>
        
      </Route>
    </Switch>
  </div>
  )
}

export default App;
