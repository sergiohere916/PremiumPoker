import React, { useEffect, useState } from "react";
import io from "socket.io-client";



function Game({gameData, socket}) {
    // const [socket, setSocket] = useState("")
    const [turn, setTurn] = useState(1);
    const [playersChecked, setPlayersChecked] = useState(0);
    // const [shuffledDeck, setShuffledDeck] = useState([]);

    const [playerCards, setPlayerCards] = useState([])
    const [tableCards, setTableCards] = useState([])
    const [winners, setWinners] = useState([])

    // const [playerCardsDealt, setPlayerCardsDealt] = useState(false)
    const [flopDealt, setFlopDealt] = useState(false)
    const [turnDealt, setTurnDealt] = useState(false)
    const [riverDealt, setRiverDealt] = useState(false)

    //INITIATING NEW GAME SET UP
    //Player cards only exists on the front end on back they are stored
    //within playerlist
    const [game, setGame] = useState({
        id: "",
        game_started: false,
        player_list: [],
        player_data: [],
        player_cards: [],
        player_cash: 0,
        table_cards: [],
        deck: [],
        last_card_dealt: 0,
        player_order: [],
        current_turn: "",
        turn_number: 0,
        player_cards_dealt: false,
        flop_dealt: false,
        turn_dealt: false,
        river_dealt: false,
        min_bet: 1,
        betting_round: "",
        flop_bets_taken: false,
        flop_bets_completed: false,
        bet_difference: 0
    })

    const [myBet, setMyBet] = useState(0)
    const [displayBetting, setDisplayBetting] = useState(false)
    //SOCKET COMMANDS -----------------------------------------
    
    socket.on('starting', (data) => {
        const user = gameData["user"]
        const money = data["player_data"][user]["cash"]
        
        //Keeping playercards within the gamedata
        const updatedGame = {...game, ...data, player_cash: money}
        setGame(updatedGame)
    })
    
    // socket.on('shuffleDeck', (deck) => {
    //     setShuffledDeck(deck);
    // })

    socket.on('dealing', (data) => {
        if (gameData["user"] === data["user"]) {
            setGame({...game, player_cards: data["cards"], player_cards_dealt: true})
            // setPlayerCards(data["cards"])
            // setPlayerCardsDealt(true)
        }
    })

    socket.on("dealing_flop", (data) => {
        // console.log("THIS IS THE FLOP ON THE FRONT END: ")
        // console.log(data);
        setGame({...game, table_cards: data["table_cards"], flop_dealt: true })

        // setTableCards(data["table_cards"])
        // setFlopDealt(true)
    })

    socket.on("dealing_turn", (data) => {
        setGame({...game, table_cards: data["table_cards"], turn_dealt: true})

        // setTableCards(data["table_cards"])
        // setTurnDealt(true)
    })

    socket.on("dealing_river", (data) => {
        // console.log(data)

        setGame({...game, table_cards: data["table_cards"], river_dealt: true})
        // setTableCards(data["table_cards"])
        // setRiverDealt(true)
    })

    socket.on("take_bet", (data) => {
        if (data["user"] === gameData["user"]) {
            setDisplayBetting(true)
            setGame({...game, bet_difference: data["bet_difference"]})
            //SHOW THE FORM
            //SET GAME flops bets taken to true
            //Bet difference needed to determine minimum needed to achieve call
        }
    })

    socket.on("returning_winners", (data) => {
        // console.log(data)
    } )


    //CHECKING VISUALS AND DEBUGGING ---------------------------
    // console.log(game["deck"]);
    // console.log(game["player_cards"])
    // console.log(tableCards)
    console.log(game)
    
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
            //May need to make shuffle deck into a function for later on
            // socket.emit("shuffleDeck", {deck: cards, room: gameData["room"]} );
            
            socket.emit('start_game', {deck: cards, room: gameData["room"]});
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

    function takeBets() {
        socket.emit("initiate_betting", {room: gameData["room"]})
    }

    function handleBetChange(e) {
        const value = e.target.value;
        setMyBet(value);
    }

    function handleBetSubmit(e) {
        e.preventDefault()
        let status = ""
        if (myBet === game["player_cash"]) {
            status = "all_in"
        } else if (myBet > game["bet_difference"]) {
            status = "raise"
        } else if (myBet === game["bet_difference"] ) {
            status = "call"
        }
        socket.emit("handle_bet_action", {room: gameData["room"], bet_status: status, bet: myBet })
        setDisplayBetting(false)
    }
    //GAME LOGIC -------------------------------------------------


    if (game["game_started"]) {
        if (!game["player_cards_dealt"]) {
            dealPlayerCards(1)
        }
        if (!game["flop_dealt"] && game["player_cards_dealt"]) {
            console.log("This flop is going to emit....")
            dealFlop(2)
        }
        if (!game["flop_bets_taken"] && game["flop_dealt"]) {
            setTimeout(takeBets, 1000)
        }
        if (!game["turn_dealt"] && game["flop_dealt"] && game["flop_bets_completed"]) {
            setTimeout(dealTurn, 2000)
        }
        if (!game["river_dealt"] && game["turn_dealt"]) {
            setTimeout(dealRiver, 2000)
        }
        if (game["player_cards"] && game["flop_dealt"] && game["river_dealt"] ) {
            checkWin()
        }
        //Remove player or continue
        // dealTableCards()

    }

    const displayPlayerHand = game["player_cards"].map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

    const displayTableCards = game["table_cards"].map((card) => {
        return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    })

    return (
        <div>
            This is our game page.
            {game["game_started"]? (<button>End Game</button>): (<button onClick={startGame}>Start Game</button>)}
            {/* <button onClick={shuffleCards}>Shuffle Deck</button> */}
            <div id="table">
               {displayTableCards}
            </div>
            <div id="playerHand">
                {displayPlayerHand}
            </div>
            {/* Set constraint on form to not allow lower bet than needed */}
            {displayBetting? 
            (<form onSubmit={handleBetSubmit}>
                <label>Bet Amount:</label>
                <input type="number" min={game["bet_difference"]} max = {game["player_cash"]} value = {myBet} onChange={handleBetChange}/>
                <button type="submit">Place Bet</button>
            </form>): 
            <>
            </>
            }
        </div>
    )
}

export default Game