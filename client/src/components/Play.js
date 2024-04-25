import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";
import Header from "./Header";


function Play({fillGameData, loggedInUser, logoutUser, roomCode1, joinCode1, updateGuestUsername, updateGuestUserId, updateGuestUserImage, updateRoomCode, updateJoinCode}) {

    // const [rooms, setRooms] = useState([])

    // const [roomCode, setRoomCode] = useState("")
    // const [joinCode, setJoinCode] = useState("")
    // const [userName, setUserName] = useState("")
    // const [userId, setUserId] = useState("")

    const [allRooms, setAllRooms] = useState([]);
    const [gameError, setGameError] = useState("");


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
        } else {
            setGameError("You Must Enter your Player Info or login before joining a game")
        } 
    }

    function addGameData() {
        if (joinCode1 !== "" && loggedInUser["username"] !== "" && loggedInUser["user_id"] !== "") {
            fillGameData(loggedInUser, joinCode1);
        } else {
            setGameError("You Must Enter your Player Info or login before joining a game")
        }
    }

    function joinRoom(roomId) {
        if (loggedInUser["username"] !== "" && loggedInUser["user_id"] !== "") {
            updateJoinCode(roomId);
            fillGameData(loggedInUser, roomId);
        } else {
            setGameError("You Must Enter your Player Info or login before joining a game")
        }
    }

    function updatePlayerImage(image) {
        updateGuestUserImage(image)
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
            <div>
                <button onClick={() => {joinRoom(roomData["room_id"])}}>Join Game</button>
            </div>
         </div>)
    })

    return (
    <div id="playPage">
    <div id="homeMenu">
        <Header id="homeMenuHeader" loggedInUser={loggedInUser} logoutUser={logoutUser} />
        {/* <NavLink to="/shop">Store</NavLink>
        <NavLink to="/login">Login</NavLink>
        <NavLink to="/inventory">Inventory</NavLink> */}
    </div>
    <div id="gameSetUp">
        <div id="gameSetUpInfo">
            <div id="requiredGameDataTitle">
                <h4>ENTER YOUR PLAYER INFO</h4>
            </div>
            <div id="requiredGameData">
                <div id="dataForm">
                    <div className="inputBox">
                        {loggedInUser["username"]? (<label>Username : </label>): (<label>Create Username: </label>)}
                        <input type="text" name="userName" value={loggedInUser["username"]} readOnly={false} onChange={(e) => updateGuestUsername(e.target.value)}/>
                    </div>
                    {/* <br/> */}
                    
                    <div className="inputBox">
                        <input type="text" name="userId" value={loggedInUser["user_id"]} readOnly={true}/>
                        {loggedInUser["user_id"]? (<button>Player Id</button>): (<button onClick={generateUID}>Generate Unique Player Id</button>)}
                    </div>
                    {/* <br/> */}

                    <div className="inputBox">
                        <input type="text" name="roomCode" value={roomCode1} readOnly={true}/>
                        <button onClick={generateCode}>Generate Room Code</button>
                        <button onClick={saveGameData}>Start A Game</button>
                    </div>
                    {/* <br/> */}

                    <div className="inputBox">
                        <input type="text" name="joinCode" value={joinCode1} onChange={(e) => updateJoinCode(e.target.value)}/>
                        <button onClick={addGameData}>Join Game using Code</button>
                    </div>
                    {/* <br/> */}

                    {/* <div></div>
                    <label>Current Icon: </label>
                    <div id="currIcon">
                        <img src={loggedInUser["image_url"]} alt="selectedIconImage"/>
                    </div> */}
                </div>
                <div id="gameDataIcon">
                    <label>Current Icon: </label>
                    <div id="currIcon">
                        <img src={loggedInUser["image_url"]} alt="selectedIconImage"/>
                    </div>
                </div>
                <div id="gameDataError">
                    {gameError}
                    {/* Error: You Must Enter your Player Info or login before joining a game. */}
                </div>
            </div>
            <div id="iconSelectTitle">
                
                <h4>SELECT YOUR ICON</h4>
            </div>
            <div id="iconSelect">
                <div id="icons">
                <div id="selectableIcons1">
                    <div className="guestIconCards">
                        <img src="https://www.svgrepo.com/show/382102/male-avatar-boy-face-man-user-8.svg" alt="fishIcon" onClick={() => {updatePlayerImage("https://www.svgrepo.com/show/382102/male-avatar-boy-face-man-user-8.svg")}}/>
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
                        <img src="https://cdn1.iconfinder.com/data/icons/graphorama-playing-cards-3/80/spades_king-512.png" alt="kingIcon" onClick={() => {updatePlayerImage("https://cdn1.iconfinder.com/data/icons/graphorama-playing-cards-3/80/spades_king-512.png")}}/>
                    </div>
                    <div className="guestIconCards">
                        {/* <img src="https://st2.depositphotos.com/2400497/8689/v/950/depositphotos_86892082-stock-illustration-angry-fish-cartoon.jpg" alt="fishIcon"/> */}
                        <img src="https://cdn1.iconfinder.com/data/icons/graphorama-playing-cards-3/80/diamonds_queen-512.png" alt="fishIcon"/>
                    </div>
                </div>
                </div>
            </div>
        </div>
        <div id="allRoomsContainer">
            <div className="roomContainerLabels">
                    <div>Room Code</div>
                    <div>Players</div>
                    <div>Join</div>
            </div>
            <div id="rooms">
                {displayAllRooms}
            </div>
            <div id="allRoomsCards">
                <img src="https://pics.clipartpng.com/Four_Aces_Cards_PNG_Clipart-1031.png" alt="quadAces"/>
            </div>
            <div id="allRoomsPokerChips">
                <img src="https://i.pinimg.com/originals/64/36/44/643644be80473b0570920700e80fd36f.png" alt="redPokerChips"/>
            </div>
        </div>
        <div id="ads">
            <div className="playAds">
                <img src="https://is2-ssl.mzstatic.com/image/thumb/Purple122/v4/1e/75/df/1e75df10-4f6d-7732-9266-7ecc0d516c0b/source/512x512bb.jpg" alt="chipsAndCards"/>
            </div>
            <div className="adCaption">
                FREE ONLINE POKER
            </div>
            <div className="playAds">
                <img src="https://media.istockphoto.com/id/921474994/vector/gambling-chip-flat-design-casino-icon-with-side-shadow.jpg?s=612x612&w=0&k=20&c=C6pKtyunExqdWyzebtbryQV5L-J13e7vQbnXglxESRo=" alt="pokerLive"/>
            </div>
            <div className="adCaption">
                EARN POINTS AND BUY PRIZES
            </div>
            <div className="playAds">
                <img src="https://m.media-amazon.com/images/I/81fvGZ5WnQL.png" alt="texasHoldemPoker"/> 
            </div>
            <div className="adCaption">
                TEXAS HOLDEM STYLE POKER
            </div>
            <div className="playAds">
                <img src="https://assets.funnygames.org/8/114048/100675/672x448/poker-with-friends.webp" alt="pokerWithFriends"/>
            </div>
            <div className="adCaption">
                INVITE FRIENDS FOR MORE FUN
            </div>
        </div>
        
    </div>
    </div>
    )
}

export default Play

// src="https://play-lh.googleusercontent.com/hU_xylni2Kvti1Cq5Wo9APQ9wBeAvFWV1Tacb4n2O2H5VviHKcFOog-FuZPYjCBeu1MH"
// src="https://play-lh.googleusercontent.com/SpWmnjazS6Z_bmyUt5zhGmoNTsMI7JFO2leT5z1jO7KLibhjJ0f-Q9fAFJWDEEdsUpM"