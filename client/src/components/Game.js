import React, { useEffect, useState } from "react";
import io from "socket.io-client";



function Game({gameData, socket}) {
    // const [socket, setSocket] = useState("")
    const [turn, setTurn] = useState(1);
    const [playersChecked, setPlayersChecked] = useState(0);
    const [shuffledDeck, setShuffledDeck] = useState([]);
    const [gameStarted, setGameStarted] = useState(false)
    

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
        }
    })


    console.log(shuffledDeck);
    
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

    //GAME LOGIC -------------------------------------------------

    if (gameStarted) {
        dealPlayerCards(1)
        // dealFlop()
        //Remove player or continue
        // dealTableCards()

    }

    return (
        <div>
            This is our game page.
            {gameStarted? (<button>End Game</button>): (<button onClick={startGame}>Start Game</button>)}
            {/* <button onClick={shuffleCards}>Shuffle Deck</button> */}
            <div id="table"></div>
        </div>
    )
}

export default Game