import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Homepage({fillGameData}) {

    const [rooms, setRooms] = useState([])

    const [roomCode, setRoomCode] = useState("")
    const [joinCode, setJoinCode] = useState("")
    const [userName, setUserName] = useState("")
    const [userId, setUserId] = useState("")

    function generateCode() {
        fetch("/room_codes")
        .then(res => res.json())
        .then(code => setRoomCode(code["room_code"]))
    }

    function generateUID() {
        if (userId === "") {
            fetch("/player_ids")
            .then(res => res.json())
            .then(uid => setUserId(uid["user_id"]))
        }
    }

    function saveGameData() {
        if (roomCode !== "" && userName !== "" && userId !== "") {
            fillGameData(userName, roomCode, userId);
        } 
    }

    function addGameData() {
        if (joinCode !== "" && userName !== "" && userId !== "") {
            fillGameData(userName, joinCode, userId);
        }
    }


    return (
    <>
    <div id="homeMenu">
        <NavLink to="/shop">Store</NavLink>
        <NavLink to="/login">Login</NavLink>
    </div>
    <div>
        <label>Create UserName: </label>
        <input type="text" name="userName" value={userName} readOnly={false} onChange={(e) => setUserName(e.target.value)}/>
        <br/>
        <input type="text" name="userId" value={userId} readOnly={true}/>
        <button onClick={generateUID}>Generate Unique Player Id</button>
        <br/>
        <input type="text" name="roomCode" value={roomCode} readOnly={true}/>
        <button onClick={generateCode}>Generate Room Code</button>
        <button onClick={saveGameData}>Start A Game</button>
        <br/>
        <input type="text" name="joinCode" value={joinCode} onChange={(e) => setJoinCode(e.target.value)}/>
        <button onClick={addGameData}>Join Game using Code</button>
    </div>
    </>
    )
}

export default Homepage