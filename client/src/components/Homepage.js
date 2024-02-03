import React, { useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Homepage({fillGameData}) {

    const [roomCode, setRoomCode] = useState("")
    const [joinCode, setJoinCode] = useState("")
    const [userName, setUserName] = useState("")

    function generateCode() {
        fetch("/room_codes")
        .then(res => res.json())
        .then(code => setRoomCode(code["room_code"]))
    }

    function saveGameData() {
        fillGameData(userName, roomCode)
    }

    function addGameData() {
        fillGameData(userName, joinCode)
    }

    return (
    <div>
        <label>Create UserName: </label>
        <input type="text" name="userName" value={userName} onChange={(e) => setUserName(e.target.value)}/>
        <br/>
        <input type="text" name="roomCode" value={roomCode}/>
        <button onClick={generateCode}>Generate Room Code</button>
        <button onClick={saveGameData}>Start A Game</button>
        <br/>
        <input type="text" name="joinCode" value={joinCode} onChange={(e) => setJoinCode(e.target.value)}/>
        <button onClick={addGameData}>Join Game using Code</button>
       
    </div>)
}

export default Homepage