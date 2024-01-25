import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import Timer from "./Timer"

function Game({gameData, socket}) {
    // const [socket, setSocket] = useState("")
    const [seconds, setSeconds] = useState(0);

    const [turn, setTurn] = useState(1);
    const [playersChecked, setPlayersChecked] = useState(0);
    const [shuffledDeck, setShuffledDeck] = useState([]);
    const [gameStarted, setGameStarted]  = useState(false)

    const [playerCards, setPlayerCards] = useState([])
    const [tableCards, setTableCards] = useState([])
    const [winners, setWinners] = useState([])
    const [user, setUser] = useState({cards : []})
    const [currentTurn, setCurrentTurn] = useState("")
    const [playerOrder, setPlayerOrder] = useState([])
    const [lastPlay, setLastPlay] = useState("")
    const [played, setPlayed] = useState("")

    const [playerCardsDealt, setPlayerCardsDealt] = useState(false)
    const [blindsPicked, setBlindsPicked] = useState(false)
    const [flopDealt, setFlopDealt] = useState(false)
    const [turnDealt, setTurnDealt] = useState(false)
    const [riverDealt, setRiverDealt] = useState(false)
    const [bettingRound, setBettingRound] = useState(false)
    const [betted, setBetted] = useState(false)

    //SOCKET COMMANDS -----------------------------------------
    
    socket.on('starting', (message) => {
        if (message === "start") {
            setGameStarted(true)
        }
    })
    
    socket.on('shuffleDeck', (deck) => {
        setShuffledDeck(deck);
    })

    socket.on('dealing', (data) => {
        if (gameData["user"] === data["user"]) {
            console.log(data);
            console.log(data["user"])
            setUser(data["user_info"])
            // setPlayerCards(data["user_info"]["cards"])
            setPlayerCardsDealt(true)
        }
    })

    socket.on("dealing_flop", (data) => {
        console.log("THIS IS THE FLOP ON THE FRONT END: ")
        console.log(data["table_cards"]);
        setTableCards(data["table_cards"])
        setFlopDealt(true)
        setBetted(false)
    })

    socket.on("dealing_turn", (data) => {
        // console.log(data)
        setTableCards(data["table_cards"])
        setTurnDealt(true)
        setBetted(false)
    })

    socket.on("dealing_river", (data) => {
        // console.log(data)
        setTableCards(data["table_cards"])
        setRiverDealt(true)
        setBetted(false)
        
    })

    socket.on("returning_winners", (data) => {
        // console.log(data)
    } )

    socket.on("blinds_picked", (data) => {
        console.log(data)
        setCurrentTurn(data["current_turn"])
        setPlayerOrder(data["player_order"])
        setLastPlay(data["last_play"])
        setBlindsPicked(true)

    })

    // socket.on("called", (data) => {
    //     if (gameData["user"] === data["user"]) {
    //         console.log(data)
    //         setPlayed("call")
    //         setUser(data["user_info"])
    //     }
    // })

    socket.on("take_bet", (data) => {
        if (currentTurn === gameData["user"]) {

            // allow the current turn to play something
            socket.emit("bet_status", {room : gameData["room"], status : played})
        }
    })

    console.log('USER')
    console.log(user)
    console.log("SHUFFLED DECK")
    console.log(shuffledDeck);
    console.log("PLAYER CARDS")
    console.log(playerCards)
    console.log("TABLE CARDS")
    console.log(tableCards)
    console.log("PLAYER ORDER")
    console.log(playerOrder)
    
    useEffect(() => {
        socket.emit('join_room', gameData)
    }, [])
    
    //FUNCTIONS ------------------------------------------------

    function startGame() {
        fetch("/cards")
        .then(res => res.json())
        .then(cards => {
            //Fisher-Yates alorith
            
            for (let i = cards.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                const temp = cards[i];
                cards[i] = cards[j];
                cards[j] = temp;
            }
    
            socket.emit("shuffleDeck", {deck: cards, room: gameData["room"]} );
            // setGameStarted(true)
            socket.emit('start_game', {message: "start", room: gameData["room"]});
        })
        

    }

    function dealPlayerCards(turn_number) {
        socket.emit("deal_cards", {room: gameData["room"], turn: turn_number});
    }


    function dealFlop(turn_number) {
        socket.emit("deal_flop", {room: gameData["room"], turn: turn_number} )
    }

    function dealTurn() {
        socket.emit("deal_turn", {room: gameData["room"]})
    }

    function dealRiver() {
        socket.emit("deal_river", {room: gameData["room"]})
    }

    function checkWin() {
        socket.emit("check_win", {room: gameData["room"]})
    }

    function pickBlinds() {
        socket.emit("pick_blinds", {room: gameData["room"]});
    }

    function betting() {
        console.log("BETTING RIGHT NOW")
        // socket.emit("betting", {room: gameData["room"], user : gameData["user"]});
        // console.log(gameData["user"])
        // console.log("CURRENT TURN: " + currentTurn)
        // let i = playerOrder.indexOf(currentTurn)
        // let x = 1
        
        // console.log("STARTING BETTING-----")
        // console.log("LAST PLAY: " + playerOrder.indexOf(lastPlay))
        // while(x < 3) {
        //     console.log(`${playerOrder[i]}'s turn`)
        //     if (i === (playerOrder.length - 1)) {
        //         i = 0
        //     } else {
        //         i++
        //         x++
        //     }
        // }
        // while(true) {
        //     console.log(`${currentTurn}'s Turn`)
        //     if (playerOrder[i] === lastPlay) {
        //         break;
        //     }
        //     if (i === (playerOrder.length - 1)) {
        //         i = 0
        //     }
        //     i++
        socket.emit("betting", {room: gameData["room"]})
        setBettingRound(true)
    }


    function bettingOver(value) {
        console.log("bruhuhasuhdfaushf")
        console.log(bettingRound)
        console.log("foisjdfosijfosij")
        setBettingRound(false)
    }

    function betConfimation(value) {
        setBetted(value)
    }

    //GAME LOGIC -------------------------------------------------

    console.log("BETTING VALUE : " + bettingRound)

    if (gameStarted) {
        if (!blindsPicked) {
            pickBlinds()
        }
        if (!playerCardsDealt && blindsPicked) {
            dealPlayerCards(1)
        }
        if (betted === false && blindsPicked && bettingRound === false && playerCardsDealt) {
            setTimeout(betting, 2000)
        }
        if (!flopDealt && playerCardsDealt && betted === true) {
            console.log("This flop is going to emit....")
            dealFlop(2)
        }
        if (!turnDealt && flopDealt && betted === true) {
            setTimeout(dealTurn, 2000)
        }
        if (!riverDealt && turnDealt && betted === true) {
            setTimeout(dealRiver, 2000)
        }
        if (playerCardsDealt && flopDealt && riverDealt && betted === false) {
            checkWin()
        }
        //Remove player or continue
        // dealTableCards()
    }

    const displayPlayerHand = user["cards"].map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

    const displayTableCards = tableCards.map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

    function handleCall() {
        setPlayed("call")
    }

    function handleFold() {
        setPlayed("fold")
    }
    
    function handleRaise() {
        setPlayed("raise")
    }

    return (
        <div>
            This is our game page.
            {gameStarted? (<button>End Game</button>): (<button onClick={startGame}>Start Game</button>)}
            {/* <button onClick={shuffleCards}>Shuffle Deck</button> */}
            <div id="table">
               {displayTableCards}
            </div>
            <div id="playerHand">
                {displayPlayerHand}
            </div>
            <div>
                {"CASH: $" + user["cash"]}
            </div>
            <div id="buttons">
                <button id="call" onClick={handleCall}>Call</button>
            </div>
            {bettingRound ? <Timer betConfimation={betConfimation} bettingOver={bettingOver}/> : ""}
        </div>
    )
}

export default Game