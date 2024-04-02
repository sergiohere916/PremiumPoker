import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Play({fillGameData, loggedInUser, roomCode1, joinCode1, updateGuestUsername, updateGuestUserId, updateRoomCode, updateJoinCode}) {

    // const [rooms, setRooms] = useState([])

    // const [roomCode, setRoomCode] = useState("")
    // const [joinCode, setJoinCode] = useState("")
    // const [userName, setUserName] = useState("")
    // const [userId, setUserId] = useState("")

    const [allRooms, setAllRooms] = useState([]);


    useEffect(() => {
        fetch("/game_rooms")
        .then(res => res.json())
        .then(roomData => {
            console.log("Here is fetched room data")
            console.log(roomData["game_rooms"])
            setAllRooms(roomData["game_rooms"])
        })
    }, [])

    function generateCode() {
        fetch("/room_codes")
        .then(res => res.json())
        .then(code => updateRoomCode(code["room_code"]))
    }

    function generateUID() {
        if (loggedInUser["user_id"] === "") {
            fetch("/player_ids")
            .then(res => res.json())
            .then(uid => updateGuestUserId(uid["user_id"]))
        }
    }

    function saveGameData() {
        if (roomCode1 !== "" && loggedInUser["username"] !== "" && loggedInUser["user_id"] !== "") {
            fillGameData(loggedInUser, roomCode1);
        } 
    }

    function addGameData() {
        if (joinCode1 !== "" && loggedInUser["username"] !== "" && loggedInUser["user_id"] !== "") {
            fillGameData(loggedInUser, joinCode1);
        }
    }

    function joinRoom(roomId) {
        updateJoinCode(roomId);
        fillGameData(loggedInUser, roomId);
    }

    const displayAllRooms = allRooms.map((roomData) => {
        // console.log(roomData["room_id"]);
        return (
        <div className="roomContainer" key={roomData["room_id"]}>
           
            <div className="roomContainerIds">
                {roomData["room_id"]}:
            </div>
            <div className="roomContainerPlayers">
                {roomData["total_players"]} / 6
            </div>
            <button onClick={() => {joinRoom(roomData["room_id"])}}>Join Game</button>
         </div>)
    })

    return (
    <>
    <div id="homeMenu">
        <NavLink to="/shop">Store</NavLink>
        <NavLink to="/login">Login</NavLink>
        <NavLink to="/inventory">Inventory</NavLink>
    </div>
    <div id="gameSetUp">
        <div id="allRoomsContainer">
            <div className="roomContainerLabels">
                    <div>Room Code</div>
                    <div>Players</div>
                    <div>Join</div>
            </div>
            {displayAllRooms}
        </div>
        <div id="gameSetUpInfo">
            {loggedInUser["username"]? (<label>Username : </label>): (<label>Create Username: </label>)}
            {/* <label>Create UserName: </label> */}
            <input type="text" name="userName" value={loggedInUser["username"]} readOnly={false} onChange={(e) => updateGuestUsername(e.target.value)}/>
            <br/>
            <input type="text" name="userId" value={loggedInUser["user_id"]} readOnly={true}/>
            {loggedInUser["user_id"]? (<button>Player Id</button>): (<button onClick={generateUID}>Generate Unique Player Id</button>)}
            {/* <button onClick={generateUID}>Generate Unique Player Id</button> */}
            <br/>
            <input type="text" name="roomCode" value={roomCode1} readOnly={true}/>
            <button onClick={generateCode}>Generate Room Code</button>
            <button onClick={saveGameData}>Start A Game</button>
            <br/>
            <input type="text" name="joinCode" value={joinCode1} onChange={(e) => updateJoinCode(e.target.value)}/>
            <button onClick={addGameData}>Join Game using Code</button>
            <div id="iconSelect">

            </div>
        </div>
        
    </div>
    </>
    )
}

export default Play