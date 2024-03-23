import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Game from "./Game";
import Homepage from "./Homepage";
import io from "socket.io-client";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Login from "./Login"
import Signup from "./Signup";
import Shop from "./Shop"
import Inventory from "./Inventory";

const socket = io("http://localhost:5555");
function App() {
  
  const [gameData, setGameData] = useState({})
  const history = useHistory()
  const [userIcons, setUserIcons] = useState([])
  const [userTags, setUserTags] = useState([])
  const [loggedInUser, setLoggedInUser] = useState({
    icon: "",
    points: 0,
    total_points: 0,
    username: "",
    user_id: "",
    type: "GUEST",
    // icon_using: "",
    // tag_using: ""
  })
  
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

  // useEffect(() => {
  //   console.log(loggedInUser["id"])
  //   fetch(`/usericons/${loggedInUser["id"]}`)
  //   .then(response => response.json())
  //   .then(userIconData => {
  //       let userIconsHolding = []
  //       for (let i = 0; i < userIconData.length; i++) {
  //         userIconsHolding.push(userIconData[i]["icon"])
  //       }
  //       setUserIcons(userIconsHolding)
  //       fetch(`/usertags/${loggedInUser["id"]}`)
  //       .then(response => response.json())
  //       .then(userTagData => {
  //         console.log(userTagData)
  //         let userTagHolding = []
  //         for (let i = 0; i < userTagData.length; i++) {
  //           userTagHolding.push(userTagData[i]["tag"])
  //         }

  //         setUserTags(userTagHolding)
  //       })
  //       .catch(error => {
  //         console.log(error)
  //       })
  //   })
  //   .catch(error => {
  //     console.log(error)
  //   })
  // }, [loggedInUser])


  function restoreGameData(user, code, userId) {
    setGameData({"user": user, "room": code, "userId": userId})
  }

  function onLogin(thisUser) {
    console.log(thisUser)
    
    setLoggedInUser({...thisUser, type: "MEMBER"})

    let userIconsHolding = []
    for (let i = 0; i < thisUser["usericons"].length; i++) {
      userIconsHolding.push(thisUser["usericons"][i]["icon"])
    }
    setUserIcons(userIconsHolding)

    let userTagHolding = []
    
    for (let i = 0; i < thisUser["usertags"].length; i++) {
      userTagHolding.push(thisUser["usertags"][i]["tag"])
    }
    setUserTags(userTagHolding)
    
  }

  // User icons is an array of objects of all the icons the user owns
  // same with tag.
  console.log(userTags)
  console.log(userIcons)

  console.log(loggedInUser)
  
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
        <Login onLogin={onLogin}></Login>
      </Route>
      <Route exact path="/signup">
        <Signup onLogin={onLogin}></Signup>
      </Route>
      <Route exact path="/shop">
        <Shop loggedInUser={loggedInUser} userIcons={userIcons} userTags={userTags} onLogin={onLogin}></Shop>
      </Route>
      <Route exact path="/inventory">
        <Inventory loggedInUser={loggedInUser} userIcons={userIcons} userTags={userTags}></Inventory>
      </Route>
    </Switch>
  </div>
  )
}

export default App;
// userIcons={userIcons} userTags={userTags}