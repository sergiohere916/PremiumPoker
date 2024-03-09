import React, { useEffect, useState } from "react";


//RETURN POINT 2/29 fixing in id into game and players ----- //
//Re add socket back here as the prop passed down if necessary
function Game({gameData, socket, restoreGameData}) {

    // const [shuffledDeck, setShuffledDeck] = useState([]);
    const [cash, setCash] = useState(0)

    //INITIATING NEW GAME SET UP
    const [game, setGame] = useState({
        id: "",
        game_started: false,
        host: "",
        player_map: {},
        player_data: {},
        player_cards: [],
        player_cash: 0,
        all_player_cards: [],
        table_cards: [],
        deck: [],
        last_card_dealt: 0,
        player_ids: [],
        player_order: [],
        round_order: [],
        current_turn: 0,
        turn_number: 0,
        player_cards_dealt: false,
        player_cards_dealing: false,
        player_cards_dealing: false,
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

        min_all_in: [],
        pots: [],
        bets: [],
        main_pot: true,
        small_blind_bet: "",
        big_blind_bet: "",
        time: 15,

        bet_difference: 0,
        disconnected_players: [],
        betting_index: 0,
        winners_declared: false,
        winners: [],
        game_over: false
    })
    
    
    const [myBet, setMyBet] = useState(0);
    const [displayBetting, setDisplayBetting] = useState(false);
    const [timer, setTimer] = useState("15");
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
                restoreGameData(data["user"], data["room"], data["userId"])
                // socket.emit('join_room', {"user": data["user"], "room": data["room"]});
                //Must add failed condition if session brings back nothing...
            })
        } else {
            console.log("joining the rooom......")
            socket.emit('join_room', gameData)
        }
    }, [gameData])

    useEffect(() => {
        socket.on('rejoin_at_bet', (data) => {
            console.log("received rejoin at bet")
            // console.log(data["game"])
            if (gameData["user"] === data["userId"]) {
                console.log("you have rejoined...")
                setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"] }))
                setDisplayBetting(true)
                setTimer(Number(data["time"]))
            }
        })

        socket.on("rejoin_game", (data) => {
            if (gameData["user"] === data["userId"]) {
                console.log("rejoining game at regular in between betting rounds....")
                setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"]  }))
            }
        })


    }, [gameData, socket])

    

    useEffect(() => {

        
        socket.on('starting', (data) => {
            // const user = gameData["user"]
            // const money = data["player_data"][user]["cash"]
            
            //Keeping playercards within the gamedata

            // const updatedGame = {...game, ...data, player_cash: money}
            console.log("starting game and updating on frontend")
            setGame(prevGame => ({
                ...prevGame,
                ...data,
                // player_cash: money
            }))
        })
        
        // socket.on('dealing', (data) => {
        //     console.log("socket on dealing must run as many times as there are players")
        //     if (gameData["user"] === data["user"]) {
        //         setGame((prevGame) => ({...prevGame, player_cards: data["cards"],
        //         all_player_cards: data["all_player_cards"], 
        //         player_cards_dealt: data["player_cards_dealt"], player_cards_dealing: data["dealing"]}))
        //         // setPlayerCards(data["cards"])
        //         // setPlayerCardsDealt(true)
        //     } else {
        //         setGame(prevGame => ({...prevGame, all_player_cards: data["all_player_cards"], player_cards_dealt: data["player_cards_dealt"], player_cards_dealing: data["dealing"]}))
        //     }
        // })

        socket.on('add_player', (data) => {
            console.log(data)
            setGame(prevGame => ({...prevGame, player_data: data["player_data"], all_player_cards: data["all_player_cards"]}))
        })


        socket.on('dealing', (data) => {
            console.log("Socket on dealing received on frontend");
            setGame(prevGame => ({...prevGame, player_data: data["adding_cards"], player_cards_dealt: data["player_cards_dealt"], player_cards_dealing: data["dealing"]}))
        })

        socket.on("dealing_flop", (data) => {
            // console.log("THIS IS THE FLOP ON THE FRONT END: ")
            console.log(data);
            setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], flop_dealt: true}))
        })

        socket.on("dealing_turn", (data) => {
            setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], turn_dealt: true}))

            // setTableCards(data["table_cards"])
            // setTurnDealt(true)
        })

        socket.on("dealing_river", (data) => {
            // console.log(data)
            setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], river_dealt: true}))
        })

        socket.on("take_bet", (data) => {
            if (data["user"] === gameData["userId"]) {
                console.log("BRUUUUUUUUUUUUUUUUUUUUUUUUUH")
                setGame(prevGame => ({...prevGame, ...data["game_update"], player_cash: data["player_cash"], bet_difference: data["bet_difference"]}))
                setDisplayBetting(true)
                setMyBet(Number(data["bet_difference"]))
                setTimer(Number(data["time"]))
                
                //SHOW THE FORM
                //SET GAME flops bets taken to true
                //Bet difference needed to determine minimum needed to achieve call
            } else {
                setGame(prevGame => ({...prevGame, ...data["game_update"]}))
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
            console.log(data)
            setGame(prevGame => ({
                ...prevGame, winners: data["winners"],
                ...data["game_update"]
            }))
        } )

        socket.on("end_betting_round", (data) => {
            console.log("ending bet round")
            setDisplayBetting(false)
            setGame(prevGame => ({...prevGame, 
                // last_raise : data["game_update"]["last_raise"],
                // raise_occurred : data["game_update"]["raise_occurred"],
                // betting_round : data["game_update"]["betting_round"],
                // min_bet : data["game_update"]["min_bet"],
                // players_folded_list : data["game_update"]["players_folded_list"],
                // player_data : data["game_update"]["player_data"],
                // player_order : data["game_update"]["player_order"],
                // current_turn : data["game_update"]["current_turn"],
                // flop_bets_completed : data["game_update"]["flop_bets_completed"],
                // flop_bets_taken : data["game_update"]["flop_bets_taken"],
                // pregame_bets_taken: data["game_update"]["pregame_bets_taken"],
                // pregame_bets_completed: data["game_update"]["pregame_bets_completed"],
                // turn_bets_taken: data["game_update"]["turn_bets_taken"],
                // turn_bets_completed: data["game_update"]["turn_bets_completed"],
                // river_bets_taken: data["game_update"]["river_bets_taken"],
                // river_bets_completed: data["game_update"]["river_bets_completed"]
                ...data["game_update"],
                min_all_in: data["game_update"]["min_all_in"],
                pots: data["game_update"]["pots"],
                bets: data["game_update"]["bets"],
                main_pot: data["game_update"]["main_pot"]
            }))
    
        })

        socket.on("fold_for_player", (data) => {
            //MIGHT BE ABLE TO REPLACE THIS condition with synchronized timer that sets displaye betting to false and maybe actually displays words fold
            run_auto_fold(data["folded_player"]);
            if (game["user"] === data["folded_player"]) {
                setDisplayBetting(false)
            }
            setGame(prevGame => ({...prevGame, player_data: data["updated_player_data"]}));
            //auto fold function will just use host to send out fold for player that failed to submit response
        })
    }, [gameData, socket])


    //CHECKING VISUALS AND DEBUGGING ---------------------------
    // console.log(game["deck"]);
    // console.log(game["player_cards"])
    // console.log(tableCards)
    console.log(gameData)
    
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

            // const cards = [
            //     { name: "10", suit: "Hearts", value: 10 },
            //     { name: "3", suit: "Diamonds", value: 3 },
            //     { name: "4", suit: "Spades", value: 4 },
            //     { name: "8", suit: "Diamonds", value: 8 },
            //     { name: "5", suit: "Diamonds", value: 5 },
            //     { name: "6", suit: "Spades", value: 6 },
            //     { name: "7", suit: "Spades", value: 7 },

            //     { name: "7", suit: "Clubs", value: 7 },
            //     // { name: "9", suit: "Spades", value: 9 },

            //     { name: "3", suit: "Clubs", value: 3 },
            //     { name: "J", suit: "Spades", value: 11 },
            //     { name: "5", suit: "Hearts", value: 5 },
            //     { name: "K", suit: "Spades", value: 13 },
            //     { name: "7", suit: "Hearts", value: 7 },
            //     { name: "2", suit: "Hearts", value: 2 },
            //     { name: "3", suit: "Hearts", value: 3 },
            //     { name: "4", suit: "Hearts", value: 4 },
            //     { name: "Q", suit: "Spades", value: 12 },
            //     { name: "6", suit: "Hearts", value: 6 },
            //     { name: "A", suit: "Spades", value: 1 },
            //     { name: "8", suit: "Hearts", value: 8 },
            //     { name: "9", suit: "Hearts", value: 9 },
            //     { name: "2", suit: "Spades", value: 2 },
            //     { name: "J", suit: "Hearts", value: 11 },
            //     { name: "Q", suit: "Hearts", value: 12 },
            //     { name: "K", suit: "Hearts", value: 13 },
            //     { name: "A", suit: "Hearts", value: 1 },
            //     { name: "2", suit: "Diamonds", value: 2 },
            //     { name: "3", suit: "Diamonds", value: 3 },
            //     { name: "4", suit: "Diamonds", value: 4 },
            //     { name: "5", suit: "Diamonds", value: 5 },
            //     { name: "6", suit: "Diamonds", value: 6 },
            //     { name: "7", suit: "Diamonds", value: 7 },
            //     { name: "8", suit: "Diamonds", value: 8 },
            //     { name: "9", suit: "Diamonds", value: 9 },
            //     { name: "10", suit: "Diamonds", value: 10 },
            //     { name: "J", suit: "Diamonds", value: 11 },
            //     { name: "Q", suit: "Diamonds", value: 12 },
            //     { name: "K", suit: "Diamonds", value: 13 },
            //     { name: "A", suit: "Diamonds", value: 1 },
            //     { name: "2", suit: "Clubs", value: 2 },
            //     { name: "10", suit: "Spades", value: 10 },
            //     { name: "4", suit: "Clubs", value: 4 },
            //     { name: "5", suit: "Clubs", value: 5 },
            //     { name: "6", suit: "Clubs", value: 6 },

            //     { name: "9", suit: "Spades", value: 9 },
            //     // { name: "7", suit: "Clubs", value: 7 },

            //     { name: "8", suit: "Clubs", value: 8 },
            //     { name: "9", suit: "Clubs", value: 9 },
            //     { name: "10", suit: "Clubs", value: 10 },
            //     { name: "J", suit: "Clubs", value: 11 },
            //     { name: "Q", suit: "Clubs", value: 12 },
            //     { name: "K", suit: "Clubs", value: 13 },
            //     { name: "A", suit: "Clubs", value: 1 }
            // ];
            // socket.emit('start_game', {deck: cards, room: gameData["room"]});
        } else {
            console.log("Need 3 or more players to start the game")
        }
    }

    function dealPlayerCards(turn_number) {
        socket.emit("deal_cards", {room: gameData["room"], turn: turn_number});
    }


    function dealFlop(turn_number) {
        socket.emit("deal_flop", {room: gameData["room"]})
        // setGame({...game, flop_dealt: true})
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
        
        // if (myBet > game["bet_difference"] && game["min_bet"] !== 0 ) {
        //     status = "raise"
        // } else if (myBet > game["bet_difference"]) {
        //     status = "standard_bet"
        // } 
        
        // if (myBet === game["player_cash"]) {
        //     status = "all_in"
        // }


        // if (myBet > game["bet_difference"] && game["min_bet"] !== 0 ) {
        //     status = "raise"
        // } else if (myBet > game["bet_difference"]) {
        //     status = "standard_bet"
        // } 
        
        // if (myBet === game["player_cash"]) {
        //     status = "all_in"
        // }


        if (myBet === game["player_cash"]) {
            status = "all_in";
        } else if (myBet > game["bet_difference"]) {
            status = "raise";
        } else if (myBet === game["bet_difference"] && game["bet_difference"] !== 0) {
            status = "call";
        } else if (myBet === game["bet_difference"] && game["bet_difference"] === 0) {
            status = "check";
        }
        // console.log(myBet)
        // console.log(typeof(myBet))
        // console.log(status)
        // console.log(game["player_cash"])

        console.log(status);
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], userId: gameData["userId"], bet_status: status, bet: myBet })
        setDisplayBetting(false)
    }

    function handleCallButton() {
        if (game["min_bet"] !== 0) {
            socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], userId: gameData["userId"], bet_status: "call", bet: game["bet_difference"] })
            setDisplayBetting(false)
        }
    }

    function handleFoldButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], userId: gameData["userId"], bet_status: "fold", bet: 0})
        setDisplayBetting(false)
    }
    //Changed bet from bet: game["player_data"][gameData["user"]]["cash"] to game["player_cash"]...check if this leads to issues
    function handleAllInButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], userId: gameData["userId"], bet_status: "all_in", bet: game["player_cash"]})
        setDisplayBetting(false)
    }

    function handleCheckButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["user"], userId: gameData["userId"], bet_status: "check", bet: 0})
        setDisplayBetting(false)
    }

    function run_auto_fold(playerName) {
        console.log("is this running twice? This is auto fold...")
        socket.emit("handle_bet_action", {room: gameData["room"], user: playerName, bet_status: "fold", bet: 0});
    }

    //NEW 3/7

    useEffect(() => {
        // if (displayBetting === true) {
        //     let intervalId;
        //     let currBetDisplay = displayBetting
        //     let newTime = game["time"] -1;
        //     console.log("timer is running...")
        //     console.log(currBetDisplay)
        //     // Start the timer
        //     intervalId = setInterval(() => {
        //         // Check if betting is still displayed
        //         currBetDisplay = displayBetting
        //         console.log(currBetDisplay)
        //         if (test === true) {
        //             // If not, clear the interval and exit the function
        //             console.log("YOU BETTED IN TIME!!")
        //             clearInterval(intervalId);
        //             return;
        //         }
        
        //         // Check if playerTimer has reached zero
        //         if (newTime === 0) {
        //             // If so, display alert and clear the interval
        //             alert("OUT OF TIME!!!!!");
        //             clearInterval(intervalId);
        //             return;
        //         }
        
        //         // Update the game time
        //         newTime -= 1
        //         console.log(newTime)
        //         setGame(prevGame => ({...prevGame, time: newTime }));
        //     }, 1000);
        // }

        // console.log("DID THIS RUN???")

        // if (displayBetting === true) {
        //     let intervalId;
        //     let newTime = timer - 1;
        //     console.log("timer is running...")
        //     console.log(newTime);
        //     // Start the timer
        //     if (newTime === 0) {
        //         console.log("OUT OF TIME!!!")
        //     } else {
        //         setTimeout(() => {
        //             setTimer(newTime)
        //         }, 1000);
        //     }
        // }

        if (displayBetting === true) {
            let updateTimer;
            console.log(timer)
            if (timer === 0) {
                console.log("OUT OF TIMEEEE!!!")
            } else {
                updateTimer = setTimeout(() => {
                    setTimer(prevTimer => prevTimer - 1);
                }, 1000);
            }
            // Clear the timer when displayBetting becomes false
            return () => clearTimeout(updateTimer);
        }

    }, [timer])





    function run_timer() {
        let intervalId;
        let currBetDisplay = displayBetting
        let newTime = game["time"] -1;
        console.log("timer is running...")
        console.log(currBetDisplay)
        // Start the timer
        intervalId = setInterval(() => {
            // Check if betting is still displayed
            console.log(currBetDisplay)
            if (currBetDisplay === false) {
                // If not, clear the interval and exit the function
                console.log("YOU BETTED IN TIME!!")
                clearInterval(intervalId);
                return;
            }
    
            // Check if playerTimer has reached zero
            if (newTime === 0) {
                // If so, display alert and clear the interval
                alert("OUT OF TIME!!!!!");
                clearInterval(intervalId);
                return;
            }
    
            // Update the game time
            newTime -= 1
            console.log(newTime)
            setGame(prevGame => ({...prevGame, time: newTime }));
        }, 1000);




    }

    function shuffleAndRestart() {
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
                
                socket.emit('restart_the_game', {deck: cards, room: gameData["room"]});
            })
            
    }

    //GAME LOGIC -------------------------------------------------
    
    
    if (game["game_started"] && game["host"] === gameData["user"]) {
        // PLAYER CARDS DEALING
        if (!game["player_cards_dealt"] && !game["player_cards_dealing"]) {
            console.log("going to run deal cards")
            dealPlayerCards(1)
        }
        // PRE GAME BETTING ROUND
        if (!game["pregame_bets_taken"] && game["player_cards_dealt"]) {
            console.log("going to run allow preflop betting")
            setTimeout(takeBets, 1000)
        }
        // // FLOP DEALING
        if (!game["flop_dealt"] && game["player_cards_dealt"] && game["pregame_bets_completed"]) {
            console.log("going to run deal flop")
            dealFlop()
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
        if (!game["winners_declared"] && game["player_cards"] && game["flop_dealt"] && game["river_dealt"] && game["river_bets_completed"]) {
            checkWin()
        }
        if (game["winners_declared"] && !game["game_over"]) {
            setTimeout(shuffleAndRestart, 5000)
        }
        //Remove player or continue
        // dealTableCards()
    }

    //LOGIC FOR PLAYER HAND IF NEEDS TO BE ISOLATED -------
    // const displayPlayerHand = game["player_cards"].map((card) => {
    //     return <div key={card["value"] + card["suit"]}>{card["name"] + " " + card["suit"]}</div>
    // })
    // ----------------------------------------------------------------

    const displayTableCards = game["table_cards"].map((card) => {
        const tableCard = card["image"];

        return <div className="tableCard" key={card["value"] + card["suit"]}>
            <img src={tableCard} alt="tableCard"/>
        </div>
    })

    
    // Cards to display but will need to keep hidden until end of game if player decides to show cards
    // const displayAllPlayerCards = game["all_player_cards"].map((playerData) => {
    //     const playerName = Object.keys(playerData)[0]
    //     // if (playerName !== gameData["user"]) {
    //         let card1 = playerData[playerName][0]
    //         let card2 = playerData[playerName][1]
    //         const currCash = game["player_data"][playerName]["cash"]
    //         const currStatus = game["player_data"][playerName]["status"]
    //         if (playerName !== gameData["user"]) {
    //             card1 = {name: "?", suit: ""};
    //             card2 = {name: "?", suit: ""};
    //         }
    //         return (<div className="playerData" key={card1["name"] + card1["suit"]}>
    //             <div>{playerName}: {currStatus} </div>
    //             <div>${currCash}</div>
    //             <div>
    //                 {card1["name"] + " " + card1["suit"]}
    //             </div>
    //             <div>
    //                 {card2["name"] + " " + card2["suit"]}
    //             </div>
    //         </div>)
    //     // }
    // })

    const displayAllPlayerCards = game["all_player_cards"].map((player) => {
        const playerData = game["player_data"][player];
        const playerId = playerData["userId"];
        const playerName = playerData["user"];
        const currCash = playerData["cash"];
        const currStatus = playerData["status"];

        let card1 = playerData["cards"][0]["image"];
        let card2 = playerData["cards"][1]["image"];

        //Need another variable to be false that way at somepoint we can switch to true and show opponents cards
        if (card1 && card2 && (playerId !== gameData["userId"])) {
            card1 = "https://i.pinimg.com/originals/91/69/ef/9169ef73b3564976a7dc564d66861027.png";
            card2 = "https://i.pinimg.com/originals/91/69/ef/9169ef73b3564976a7dc564d66861027.png";
        } 
        
        const playerTurn = playerData["myTurn"]

        let betAmount = 0

        if (game["betting_round"] == "pregame") {
            betAmount = game["player_data"][player]["pregame"]
        } else if (game["betting_round"] == "flop") {
            betAmount = game["player_data"][player]["flop"]
        } else if (game["betting_round"] == "turn") {
            betAmount = game["player_data"][player]["turn"]
        } else if (game["betting_round"] == "river") {
            betAmount = game["player_data"][player]["river"]
        }
        //
        
        // if (playerTurn === true) {
        //     infoOutline = "3 px solid green";
        // }

        return (
            <div id={player}>
                {playerId? (
                <>
                {playerTurn? ( 
                <>
                <div id={player + "icon"} style={{boxShadow: "0 0 0 4px rgb(216, 214, 214), 0 0 0 10px rgb(30, 5, 88), 0 0 10px 20px rgba(255, 255, 255, 0.596)"}}>
                    <img id = {player + "img"} src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"/>
                </div>
                <div id={player + "info"} style={{border: "3px solid green"}}>
                    {player}
                    <hr/>
                    <div className="Money">Cash: ${currCash}</div>
                    <div>Last Bet: </div>         
                </div>
                </>
                ):
                (
                <>
                <div id={player + "icon"}>
                    <img id = {player + "img"} src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-oeyilDG6-xNRqwDmSgqaUe0xefnBfVNwNw&usqp=CAU"/>
                </div>
                <div id={player + "info"} >
                    {player}
                    <hr/>
                    <div className="Money">Cash: ${currCash}</div>
                    <div>Last Bet: </div>         
                </div>
                </>
                )
                }
                <div id={player + "cards"}>
                    <div className="cards12">
                        {card1? (<img src={card1} className="cardX" alt="playerCard"/>): (<></>)}
                    </div>
                    <div className="cards12">
                    {card2? (<img src={card2} className="cardX" alt="playerCard"/>): (<></>)}
                    </div>
                </div>
                </>): (
                <>
                <div id={player + "icon"}>
                    <img id = {player + "img"} src="https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg"/>
                </div>
                <div id={player + "info"}>
                    {/* <h4>{player}</h4> */}
                    {player}
                    <hr/>
                    <div>Vacant</div>    
                </div>
                {/* <div id={player + "cards"}>
                    <div className="cards12">
                        <img src="https://i.pinimg.com/originals/91/69/ef/9169ef73b3564976a7dc564d66861027.png" className="cardX"/>
                    </div>
                    <div className="cards12">
                        <img src="https://i.pinimg.com/originals/91/69/ef/9169ef73b3564976a7dc564d66861027.png" className="cardX"/>
                    </div>
                </div> */}
                </>)}
            </div>
        )
        
    })
    //yugioh image https://orig10.deviantart.net/69f2/f/2016/289/4/1/ygo_card_backing__final__by_icycatelf-dal6wsb.png

    // useEffect(() => {
    //     // This checks if the winners list of lists is greater than 0
    //     if (game["winners"].length > 0) {
    //         const interval = setInterval(() => {
    //             if (displayedWinnerIndex < game["winners"].length) {
    //                 setDisplayedWinner(game["winners"][displayedWinnerIndex]);
    //                 setDisplayedWinnerIndex(prevIndex => prevIndex + 1);
    //             } else {
    //                 setDisplayedWinner(null);
    //                 setDisplayedWinnerIndex(0);
    //                 setGame(prevGame => ({...prevGame, winners_declared: true}));
    //             }
    //         }, 3000);
    //         return () => clearInterval(interval);
    //     }
    // }, [gameData, displayedWinnerIndex]);

    const winnersDisplay = game["winners"].map((winnersList, index) => {
        console.log("THIS IS THE INDEX : " + index)
        
        let winnerdinner = ""

        for (let i = 0; i < game["winners"][index].length; i++) {
            winnerdinner += game["player_data"][game["winners"][index][i]]["user"] + " "
        }

        return (<div>
            <div>{index === game["winners"].length - 1 ? "main pot " : "side pot " + parseInt(index + 1)} : {winnerdinner}</div>
        </div>)
    })

    
    return (
        <>
        <div className="menuBar">
            <div id="exitGame">Leave Room</div>
            <div id="playerCount">Total Players:  {game["player_ids"].length} / 6</div>
            <div id="gameInfo">
                <div>Premium Poker: No Limit Holdem 5/10</div>
                <div>Room Code: {gameData["room"]}</div>
            </div>
        </div>
        <div id="gamePage">
        <div id="game">
            {/* This is our game page. */}
            {/* {game["game_started"]? (<button>End Game</button>): (<button onClick={startGame}>Start Game</button>)} */}
            
            {/* <div id="table">
                <div id="tableCards">
                    
                </div>
            </div> */}
            {/* <div id="playerHand">
                {displayPlayerHand}
            </div> */}
            {/* <hr/> */}
            <div className="container">
                <div className="icon">
                    
                    <div id="pokerLogoContainer">
                        <img id="pokerLogo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/World_Series_of_Poker_logo.svg/480px-World_Series_of_Poker_logo.svg.png" alt="pokerTableLogo" />
                    </div>
                    <div id="newTableCards">
                        {displayTableCards}
                    </div>
                    {displayAllPlayerCards}
                </div>
            
                {game["game_started"]? (<button>End Game</button>): (<div className="startButtonContainer"><button className="startButton" onClick={startGame}>Start Game</button></div>)}
                <div className="box" style={{"--c": "5px solid blue"}}>
                    {/* {displayAllPlayerCards} */}
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
                        <button onClick={handleCallButton}>{"CALL" + " $" + game["bet_difference"]}</button>
                        {game["bet_difference"] === 0? <button onClick={handleCheckButton}>CHECK</button>: <></>}
                    </div>):
                (<></>)
                }
                    {winnersDisplay}
                    {timer >= 10? (<>{`00:${timer}`}</>): (<>{`00:0${timer}`}</>)}
                </div>
            </div>
        </div>
        </div>
        </>
    )
}

export default Game