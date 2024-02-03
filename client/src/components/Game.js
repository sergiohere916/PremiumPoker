import React, { useEffect, useState } from "react";
import io from "socket.io-client";

//RESET POINT ALL THE WAY BACK TO START OF 2/7/24
//Re add socket back here as the prop passed down if necessary
function Game({gameData, socket, restoreGameData}) {

    // const [shuffledDeck, setShuffledDeck] = useState([]);
    const [cash, setCash] = useState(0)

    const [playerCards, setPlayerCards] = useState([])
    const [tableCards, setTableCards] = useState([])
    const [winners, setWinners] = useState([])


    //INITIATING NEW GAME SET UP
    //Player cards only exists on the front end on back they are stored
    //within playerlist
    const [game, setGame] = useState({
        id: "",
        game_started: false,
        host: "",
        player_list: [],
        player_data: {},
        player_cards: [],
        player_cash: 0,
        all_player_cards: [],
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
        pot: 0,
        min_bet: 0,
        betting_round: "",
        last_raise: "",
        players_folded_list: [],
        players_all_in: [],
        raise_occurred: false,
        pregame_bets_taken: false,
        pregame_bets_completed: false,
        flop_bets_taken: false,
        flop_bets_completed: false,
        turn_bets_taken: false,
        turn_bets_completed: false,
        river_bets_taken: false,
        river_bets_completed: false,
        bet_difference: 0
    })
    
    const [myBet, setMyBet] = useState(0)
    const [displayBetting, setDisplayBetting] = useState(false)
    //SOCKET COMMANDS -----------------------------------------
    // useEffect(() => {
    //     if (Object.keys(gameData).length === 0) {
    //         console.log("This should only run on refresh")
    //         fetch("/checkSession")
    //         .then(r => r.json())
    //         .then(data => {
    //             // restoreGameData(data["user"], data["room"])
    //             console.log("We are re initializing state")
    //             console.log(data)
    //             restoreGameData(data["user"], data["room"])
    //             // socket.emit('join_room', {"user": data["user"], "room": data["room"]});
    //         })
    //     } else {
    //         socket.emit('join_room', gameData)
    //     }
    // }, [])

    useEffect(() => {
        if (Object.keys(gameData).length === 0) {
            console.log("This should only run on refresh")
            fetch("/checkSession")
            .then(r => r.json())
            .then(data => {
                // restoreGameData(data["user"], data["room"])
                console.log("We are re initializing state")
                console.log(data)
                restoreGameData(data["user"], data["room"])
                // socket.emit('join_room', {"user": data["user"], "room": data["room"]});
            })
        } else {
            console.log("joining the rooom......")
            socket.emit('join_room', gameData)
        }
    }, [gameData])

    useEffect(() => {
        socket.on('rejoin_at_bet', (data) => {
            console.log("received rejoin at bet")
            console.log(data["game"])
            if (gameData["user"] === data["user"]) {
                console.log("you have rejoined...")
                setGame(prevGame => ({...prevGame, ...data["game"], player_cards: data["player_cards"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"] }))
                setDisplayBetting(true)
            }
        })

        socket.on("rejoin_game", (data) => {
            if (gameData["user"] === data["user"]) {
                setGame(prevGame => ({...prevGame, ...data["game"], player_cards: data["player_cards"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"]  }))
            }
        })


    }, [gameData])

    

        // socket.on('rejoin_at_bet', (data) => {
        //     console.log("received rejoin at bet")
        //     console.log(gameData)
        //     if (gameData["user"] === data["user"]) {
        //         console.log("you have rejoined...")
        //         const game = data["game"]
        //         setGame(prevGame => ({...prevGame, ...game}))
        //         setDisplayBetting(true)
        //     }
        // })
    
    socket.on('starting', (data) => {
        const user = gameData["user"]
        const money = data["player_data"][user]["cash"]
        
        //Keeping playercards within the gamedata

        // const updatedGame = {...game, ...data, player_cash: money}
        setGame(prevGame => ({
            ...prevGame,
            ...data,
            player_cash: money
        }))
        // setting cash
        setCash(money)
    })
    
    // socket.on('shuffleDeck', (deck) => {
    //     setShuffledDeck(deck);
    // })
    
    socket.on('dealing', (data) => {
        if (gameData["user"] === data["user"]) {
            console.log("game at the time socket on dealing of cards runs..." + "")
            console.log(game)
            console.log("game started has already reset to it's default...why?")
            setGame((prevGame) => ({...prevGame, player_cards: data["cards"],
            all_player_cards: data["all_player_cards"], 
            player_cards_dealt: data["player_cards_dealt"]}))
            // setPlayerCards(data["cards"])
            // setPlayerCardsDealt(true)
        } else {
            setGame(prevGame => ({...prevGame, all_player_cards: data["all_player_cards"], player_cards_dealt: data["player_cards_dealt"]}))
        }
    })

    socket.on("dealing_flop", (data) => {
        // console.log("THIS IS THE FLOP ON THE FRONT END: ")
        // console.log(data);
        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], flop_dealt: true }))

        // setTableCards(data["table_cards"])
        // setFlopDealt(true)
    })

    socket.on("dealing_turn", (data) => {
        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], turn_dealt: true}))

        // setTableCards(data["table_cards"])
        // setTurnDealt(true)
    })

    socket.on("dealing_river", (data) => {
        // console.log(data)

        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], river_dealt: true}))
        // setTableCards(data["table_cards"])
        // setRiverDealt(true)
    })

    socket.on("take_bet", (data) => {
        console.log(gameData)
        if (data["user"] === gameData["user"]) {
            console.log("BRUUUUUUUUUUUUUUUUUUUUUUUUUH")
            setGame(prevGame => ({...prevGame, ...data["game_update"], bet_difference: data["bet_difference"]}))
            setDisplayBetting(true)
            //SHOW THE FORM
            //SET GAME flops bets taken to true
            //Bet difference needed to determine minimum needed to achieve call
        }
    })

    socket.on("handle_cash", (data) => {
        if (data["player"] === gameData["user"]) {
            console.log(data["player_cash"])
            console.log("CASH HAS NOW BEEN UPDATED FOR " + gameData["user"])
            setGame(prevGame => ({...prevGame, ...data["game_update"], player_cash: data["player_cash"]}))
            // setCash(data["player_cash"])
        } else {
            setGame(prevGame => ({...prevGame, ...data["game_update"]}))
        }
    })

    socket.on("returning_winners", (data) => {
        // console.log(data)
    } )

    socket.on("end_betting_round", (data) => {
        setGame(prevGame => ({...prevGame, 
            last_raise : data["game_update"]["last_raise"],
            raise_occurred : data["game_update"]["raise_occurred"],
            betting_round : data["game_update"]["betting_round"],
            min_bet : data["game_update"]["min_bet"],
            players_folded_list : data["game_update"]["players_folded_list"],
            player_data : data["game_update"]["player_data"],
            player_order : data["game_update"]["player_order"],
            current_turn : data["game_update"]["current_turn"],
            flop_bets_completed : data["game_update"]["flop_bets_completed"],
            flop_bets_taken : data["game_update"]["flop_bets_taken"],
            pregame_bets_taken: data["game_update"]["pregame_bets_taken"],
            pregame_bets_completed: data["game_update"]["pregame_bets_completed"],
            turn_bets_taken: data["game_update"]["turn_bets_taken"],
            turn_bets_completed: data["game_update"]["turn_bets_completed"],
            river_bets_taken: data["game_update"]["river_bets_taken"],
            river_bets_completed: data["game_update"]["river_bets_completed"]
            // ...data["game_update"]

        }))
        setDisplayBetting(false)
    })





    //CHECKING VISUALS AND DEBUGGING ---------------------------
    // console.log(game["deck"]);
    // console.log(game["player_cards"])
    // console.log(tableCards)
    console.log(game)
    
    // useEffect(() => {
    //     socket.emit('join_room', gameData);
    // }, [])


    
    //FUNCTIONS ------------------------------------------------
    function startGame() {
        if (true) {
            fetch("/cards")
            .then(res => res.json())
            .then(cards => {
                //Fisher-Yates alorith
                console.log(cards)
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
        } else {
            console.log("Need 3 or more players to start the game")
        }
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
        const value = Number(e.target.value);
        setMyBet(value);
    }

    function handleBetSubmit(e) {
        e.preventDefault()
        let status = ""
        
        if (myBet > game["bet_difference"] && game["min_bet"] !== 0 ) {
            status = "raise"
        } else if (myBet > game["bet_difference"]) {
            status = "standard_bet"
        } 
        
        if (myBet === game["player_cash"]) {
            status = "all_in"
        }
       
        // console.log(myBet)
        // console.log(typeof(myBet))
        // console.log(status)
        // console.log(game["player_cash"])

        // if (myBet === game["player_cash"]) {
        //     status = "all_in"
        // } else if (myBet > game["bet_difference"] && game["min_bet"] !== 0 ) {
        //     status = "raise"
        // } else if (myBet === game["bet_difference"] && myBet !== 0 ) {
        //     status = "call"
        // } else if (myBet === 0) {
        //     status = "check"
        // } else if (myBet > game["bet_difference"]) {
        //     status = "standard_bet"
        // }
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], bet_status: status, bet: myBet })
        setDisplayBetting(false)
    }

    function handleCallButton() {
        if (game["min_bet"] !== 0) {
            socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], bet_status: "call", bet: game["bet_difference"] })
            setDisplayBetting(false)
        }
    }

    function handleFoldButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], bet_status: "fold", bet: 0})
        setDisplayBetting(false)
    }

    function handleAllInButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], bet_status: "all_in", bet: game["player_data"][gameData["user"]]["cash"] })
        setDisplayBetting(false)
    }

    function handleCheckButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], bet_status: "check", bet: 0})
        setDisplayBetting(false)
    }

    //GAME LOGIC -------------------------------------------------

    if (game["game_started"] && game["host"] === gameData["user"]) {
        // PLAYER CARDS DEALING
        if (!game["player_cards_dealt"]) {
            console.log("going to run deal cards")
            dealPlayerCards(1)
        }
        // PRE GAME BETTING ROUND
        if (!game["pregame_bets_taken"] && game["player_cards_dealt"]) {
            console.log("going to run allow preflop betting")
            setTimeout(takeBets, 1000)
        }
        // FLOP DEALING
        if (!game["flop_dealt"] && game["player_cards_dealt"] && game["pregame_bets_completed"]) {
            console.log("going to run deal flop")
            dealFlop(2)
        }
        // FLOP BETTING ROUND
        if (!game["flop_bets_taken"] && game["flop_dealt"]) {
            console.log("going to allow post flop betting")
            setTimeout(takeBets, 1000)
        }
        // TURN DEALING
        if (!game["turn_dealt"] && game["flop_dealt"] && game["flop_bets_completed"]) {
            console.log("going to run deal turn")
            setTimeout(dealTurn, 2000)
        }
        // TURN BETTING ROUND
        if (!game["turn_bets_taken"] && game["turn_dealt"]) {
            console.log("going to allow post turn betting")
            setTimeout(takeBets, 1000)
        }
        // RIVER DEALING
        if (!game["river_dealt"] && game["turn_dealt"] && game["turn_bets_completed"]) {
            console.log("going to run deal river")
            setTimeout(dealRiver, 2000)
        }
        // RIVER DEALING ROUND
        if (!game["river_bets_taken"] && game["river_dealt"]) {
            setTimeout(takeBets, 1000)
        }
        if (game["player_cards"] && game["flop_dealt"] && game["river_dealt"] && game["river_bets_completed"]) {
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

    
    // for (const player in game["player_data"]) {
    //     if (player !== gameData["user"] && game["player_cards_dealt"]) {
    //         const cards = game["player_data"][player]["cards"]
    //         // allPlayerCards.push(cards)
    //         if (!allPlayerCards.includes(cards)) {
    //             allPlayerCards.push(cards)
    //             setAllPlayerCards([...allPlayerCards])
    //         }
    //     }
    // }
    
    // Cards to display but will need to keep hidden until end of game if player decides to show cards
    const displayAllPlayerCards = game["all_player_cards"].map((playerData) => {
        const playerName = Object.keys(playerData)[0]
        if (playerName !== gameData["user"]) {
            const card1 = playerData[playerName][0]
            const card2 = playerData[playerName][1]
            return (<div key={card1["name"] + card1["suit"]}>
                <div>
                    {card1["name"] + " " + card1["suit"]}
                </div>
                <div>
                    {card2["name"] + " " + card2["suit"]}
                </div>
            </div>)
        }
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
            <div>
                {displayAllPlayerCards}
            </div>
            {/* Set constraint on form to not allow lower bet than needed */}
            {displayBetting ?
            (
                <div>
                    <form onSubmit={handleBetSubmit}>
                        <label>Bet Amount:</label>
                        <input type="number" min={game["bet_difference"]} max = {game["player_cash"]} value = {myBet} onChange={handleBetChange}/>
                        <button type="submit">Place Bet</button>
                    </form>
                    <button onClick={handleAllInButton}>ALL IN</button>
                    <button onClick={handleFoldButton}>FOLD</button>
                    <button onClick={handleCallButton}>CALL</button>
                    <button onClick={handleCheckButton}>CHECK</button>
                </div>):
            <>
            </>
            }
            <div>
                {"CASH: " + game["player_cash"]}
            </div>
        </div>
    )
}

export default Game