import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Homepage({fillGameData}) {

    const [rooms, setRooms] = useState([])

    const [roomCode, setRoomCode] = useState("")
    const [joinCode, setJoinCode] = useState("")
    const [userName, setUserName] = useState("")

    const [cards, setCards] = useState([""])

    function generateCode() {
        fetch("/room_codes")
        .then(res => res.json())
        .then(code => setRoomCode(code["room_code"]))
    }

    function saveGameData() {
        if (roomCode !== "" && userName !== "") {
            fillGameData(userName, roomCode);
        } 
    }

    function addGameData() {
        if (joinCode !== "" && userName !== "") {
            fillGameData(userName, joinCode);
        }
    }

    useEffect(() => {
        fetch("/cards")
        .then(res => res.json())
        .then(data => {
            setCards(data)
        })
    }, [])

    console.log(cards)

    const displayCards = cards.map(card => (
        <div key={card["value"] + card["suit"]}>
            <img src={card["image"]} alt={`${card["value"]} of ${card["suit"]}`} />
        </div>
    ));
    
    return (
    <div>
        {/* <div>
            {displayCards}
        </div> */}
        <div>
            
        </div>
        <label>Create UserName: </label>
        <input type="text" name="userName" value={userName} onChange={(e) => setUserName(e.target.value)}/>
        <br/>
        <input type="text" name="roomCode" value={roomCode} readOnly={true}/>
        <button onClick={generateCode}>Generate Room Code</button>
        <button onClick={saveGameData}>Start A Game</button>
        <br/>
        <input type="text" name="joinCode" value={joinCode} onChange={(e) => setJoinCode(e.target.value)}/>
        <button onClick={addGameData}>Join Game using Code</button>
       
    </div>)
}

export default Homepage