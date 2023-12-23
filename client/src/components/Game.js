import React, { useEffect, useState } from "react";
import io from "socket.io-client";



function Game({gameData, socket}) {
    // const [socket, setSocket] = useState("")
    const [turn, setTurn] = useState(1);
    const [playersChecked, setPlayersChecked] = useState(0);
    const [shuffledDeck, setShuffledDeck] = useState([]);
    const [gameStarted, setGameStarted] = useState(false)

    const [playerCards, setPlayerCards] = useState([])
    const [tableCards, setTableCards] = useState([])
    const [winners, setWinners] = useState([])

    const [playerCardsDealt, setPlayerCardsDealt] = useState(false)
    const [flopDealt, setFlopDealt] = useState(false)
    const [turnDealt, setTurnDealt] = useState(false)
    const [riverDealt, setRiverDealt] = useState(false)

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
            // console.log(data);
            setPlayerCards(data["cards"])
            setPlayerCardsDealt(true)
        }
    })

    socket.on("dealing_flop", (data) => {
        console.log("THIS IS THE FLOP ON THE FRONT END: ")
        console.log(data["table_cards"]);
        setTableCards(data["table_cards"])
        setFlopDealt(true)
    })

    socket.on("dealing_turn", (data) => {
        // console.log(data)
        setTableCards(data["table_cards"])
        setTurnDealt(true)
    })

    socket.on("dealing_river", (data) => {
        // console.log(data)
        setTableCards(data["table_cards"])
        setRiverDealt(true)
    })

    socket.on("returning_winners", (data) => {
        // console.log(data)
    } )

    console.log(shuffledDeck);
    console.log(playerCards)
    console.log(tableCards)
    
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
    //GAME LOGIC -------------------------------------------------


    if (gameStarted) {
        if (!playerCardsDealt) {
            dealPlayerCards(1)
        }
        if (!flopDealt && playerCardsDealt) {
            console.log("This flop is going to emit....")
            dealFlop(2)
        }
        if (!turnDealt && flopDealt) {
            setTimeout(dealTurn, 2000)
        }
        if (!riverDealt && turnDealt) {
            setTimeout(dealRiver, 2000)
        }
        if (playerCards && flopDealt && riverDealt ) {
            checkWin()
        }
        //Remove player or continue
        // dealTableCards()

    }

    const displayPlayerHand = playerCards.map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

    const displayTableCards = tableCards.map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

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
        </div>
    )
}

export default Game