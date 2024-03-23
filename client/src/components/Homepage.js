import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Homepage({fillGameData, user, roomCode1, joinCode1, updateGuestUsername, updateGuestUserId, updateRoomCode, updateJoinCode}) {

    const [rooms, setRooms] = useState([])

    const [roomCode, setRoomCode] = useState("")
    const [joinCode, setJoinCode] = useState("")
    const [userName, setUserName] = useState("")
    const [userId, setUserId] = useState("")

    function generateCode() {
        fetch("/room_codes")
        .then(res => res.json())
        .then(code => updateRoomCode(code["room_code"]))
    }

    function generateUID() {
        if (user["user_id"] === "") {
            fetch("/player_ids")
            .then(res => res.json())
            .then(uid => updateGuestUserId(uid["user_id"]))
        }
    }

    function saveGameData() {
        if (roomCode1 !== "" && user["username"] !== "" && user["user_id"] !== "") {
            fillGameData(user, roomCode1);
        } 
    }

    function addGameData() {
        if (joinCode1 !== "" && user["username"] !== "" && user["user_id"] !== "") {
            fillGameData(user, joinCode1);
        }
    }


    return (
    <>
    <div id="homeMenu">
        <NavLink to="/shop">Store</NavLink>
        <NavLink to="/login">Login</NavLink>
        <NavLink to="/inventory">Inventory</NavLink>
    </div>
    <div>
        {user["username"]? (<label>Username : </label>): (<label>Create Username: </label>)}
        {/* <label>Create UserName: </label> */}
        <input type="text" name="userName" value={user["username"]} readOnly={false} onChange={(e) => updateGuestUsername(e.target.value)}/>
        <br/>
        <input type="text" name="userId" value={user["user_id"]} readOnly={true}/>
        {user["user_id"]? (<button>Player Id</button>): (<button onClick={generateUID}>Generate Unique Player Id</button>)}
        {/* <button onClick={generateUID}>Generate Unique Player Id</button> */}
        <br/>
        <input type="text" name="roomCode" value={roomCode1} readOnly={true}/>
        <button onClick={generateCode}>Generate Room Code</button>
        <button onClick={saveGameData}>Start A Game</button>
        <br/>
        <input type="text" name="joinCode" value={joinCode1} onChange={(e) => updateJoinCode(e.target.value)}/>
        <button onClick={addGameData}>Join Game using Code</button>
    </div>
    </>
    )
}

export default Homepage