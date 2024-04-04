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
            <div id="requiredGameDataTitle">
                <h4>ENTER YOUR PLAYER INFO</h4>
            </div>
            <div id="requiredGameData">
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
            </div>
            <div id="iconSelectTitle">
                
                <h3>SELECT YOUR ICON</h3>
            </div>
            <div id="iconSelect">
                <div id="selectableIcons1">
                    <div className="guestIconCards">
                        <img src="https://www.svgrepo.com/show/382102/male-avatar-boy-face-man-user-8.svg" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                        <img src="https://www.svgrepo.com/show/382109/male-avatar-boy-face-man-user-7.svg" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                    <img src="https://www.svgrepo.com/show/382095/female-avatar-girl-face-woman-user-4.svg" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                        <img src="https://www.svgrepo.com/show/382100/female-avatar-girl-face-woman-user-7.svg" alt="fishIcon"/>
                    </div>
                </div>
                <div id="selectableIcons2">
                    <div className="guestIconCards">
                        <img src="https://cdn1.iconfinder.com/data/icons/avatars-1-5/136/87-512.png" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                        <img src="https://icon-library.com/images/avatar-icon-images/avatar-icon-images-4.jpg" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                        {/* <img src="https://st.depositphotos.com/1797973/1418/v/950/depositphotos_14187177-stock-illustration-big-angry-fish-cartoon.jpg" alt="fishIcon"/> */}
                        <img src="https://cdn1.iconfinder.com/data/icons/graphorama-playing-cards-3/80/spades_king-512.png" alt="fishIcon"/>
                    </div>
                    <div className="guestIconCards">
                        {/* <img src="https://st2.depositphotos.com/2400497/8689/v/950/depositphotos_86892082-stock-illustration-angry-fish-cartoon.jpg" alt="fishIcon"/> */}
                        <img src="https://cdn1.iconfinder.com/data/icons/graphorama-playing-cards-3/80/diamonds_queen-512.png" alt="fishIcon"/>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
    </>
    )
}

export default Play