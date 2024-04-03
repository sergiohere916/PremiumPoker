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
import Play from "./Play"
import Profile from "./Profile"
import Leaderboard from "./Leaderboard"


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
    image_url: "https://t3.ftcdn.net/jpg/06/37/09/94/360_F_637099445_5zVOcmnJNDmVe9ypWCdNg6IkcCe35xwu.jpg",
    tag:  "",
    // icon_using: "",
    // tag_using: ""
  })
  const [roomCode1, setRoomCode1] = useState("")
  const [joinCode1, setJoinCode1] = useState("")


  function updateGuestUsername(nameData) {
    setLoggedInUser(prevUser => ({...prevUser, username: nameData}))
  }

  function updateGuestUserId(userIdData) {
    setLoggedInUser(prevUser => ({...prevUser, user_id: userIdData}))
  }

  function updateRoomCode(code) {
    setRoomCode1(code)
  }

  function updateJoinCode(code) {
    setJoinCode1(code)
  }

  useEffect(() => {
    fetch("/users_points")
    .then(response => response.json())
    .then(data => {
      console.log(data)
    })
  })
  
  //If idea does not work must return socket={socket} to Game component
  function fillGameData(user, code) {
    const data = {
    "username": user["username"],
    "user_id": user["user_id"],
    "image_url": user["image_url"],
    "points": user["points"],
    "total_points": user["total_points"],
    "type": user["type"], 
    "room": code, 
    }

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

  useEffect(() => {
    fetch("/checkUserSession")
    .then((response) => {
      if (response.ok) {
        response.json().then((userData) => {

          let userIconsHolding = []
    
          for (let i = 0; i < userData["usericons"].length; i++) {
            userIconsHolding.push(userData["usericons"][i]["icon"])
          }
          setUserIcons(userIconsHolding)

          let userTagHolding = []
    
          for (let i = 0; i < userData["usertags"].length; i++) {
            userTagHolding.push(userData["usertags"][i]["tag"])
          }
          setUserTags(userTagHolding)
          setLoggedInUser({...userData, type: "MEMBER"})
        })
      } else {
        console.log("NO USER DATA AVAILABLE")
      }
    })
  }, [])
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
  function logoutUser() {
    setLoggedInUser({
      icon: "",
      points: 0,
      total_points: 0,
      username: "",
      user_id: "",
      type: "GUEST",
    })
  }

  function restoreGameData(gameData) {
    setGameData({"username": gameData["username"], "user_id": gameData["user_id"], "image_url": gameData["image_url"], "points": gameData["points"], "total_points": gameData["total_points"], "type": gameData["type"], "room": gameData["room"]})
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

  function addNewUserIcon(newIcon) {
    setUserIcons([...userIcons, newIcon["icon"]]);
  }

  function addNewUserTag(newTag) {
    setUserTags([...userTags, newTag["tag"]])
  }

  // User icons is an array of objects of all the icons the user owns
  // same with tag.

  // console.log(userTags)
  // console.log(userIcons)
  console.log(loggedInUser)
  
  return (
  <div id="page">
    <Switch>
      <Route path="/game">
        <Game gameData={gameData} socket={socket} restoreGameData={restoreGameData}/>
      </Route>
      <Route exact path="/">
        <Homepage fillGameData={fillGameData} loggedInUser={loggedInUser} logoutUser={logoutUser}/>
      </Route> 
      <Route exact path="/login">
        <Login onLogin={onLogin}></Login>
      </Route>
      <Route exact path="/signup">
        <Signup onLogin={onLogin}></Signup>
      </Route>
      <Route exact path="/shop">
        <Shop loggedInUser={loggedInUser} userIcons={userIcons} userTags={userTags} onLogin={onLogin} addNewUserIcon={addNewUserIcon} addNewUserTag={addNewUserTag}></Shop>
      </Route>
      <Route exact path="/inventory">
        <Inventory loggedInUser={loggedInUser} userIcons={userIcons} userTags={userTags} onLogin={onLogin}></Inventory>
      </Route>
      <Route exact path="/play"> 
        <Play loggedInUser={loggedInUser} roomCode1={roomCode1} joinCode1={joinCode1} updateGuestUsername={updateGuestUsername} updateGuestUserId={updateGuestUserId} updateRoomCode={updateRoomCode} updateJoinCode={updateJoinCode} fillGameData={fillGameData}></Play>
      </Route>
      <Route path="/user/:id">
        <Profile></Profile>
      </Route>
      <Route exact path="/leaderboard">
        <Leaderboard></Leaderboard>
      </Route>
    </Switch>
  </div>
  )
}

export default App;
// userIcons={userIcons} userTags={userTags}