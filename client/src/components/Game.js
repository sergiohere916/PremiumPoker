import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import luigi from "../css/LuigiPokerFinal.png"
import tableChips from "../css/images/tableChips01.png"


//RETURN POINT 2/29 fixing in id into game and players ----- //
//Re add socket back here as the prop passed down if necessary
function Game({gameData, socket, restoreGameData}) {

    const history = useHistory();
    // const [shuffledDeck, setShuffledDeck] = useState([]);
    const [cash, setCash] = useState(0)

    //INITIATING NEW GAME SET UP
    const [game, setGame] = useState({
        id: "",
        game_started: false,
        host: "",
        total_players: 0,
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
        first_better: "",
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
        total_pot: 0,
        bets: [],
        main_pot: true,
        small_blind_bet: "",
        big_blind_bet: "",
        time: 15,

        bet_difference: 0,
        disconnected_players: {},
        betting_index: 0,
        winners_declared: false,
        winners: [],
        game_over: false
    })
    
    
    const [myBet, setMyBet] = useState(0);
    const [displayBetting, setDisplayBetting] = useState(false);
    const [timer, setTimer] = useState("15");
    const [opponentBetting, setOpponentBetting] = useState(false);
    const [showRebuy, setShowRebuy] = useState(false);

   

    function sumUp(total, betObj) {
        return total["bet"] + betObj["bet"];
    }

    //DISPLAY POT PROPERLY IN GAME
    // let roundBets = game["bets"].reduce(sumUp)

    // const displayPot = game["bets"].reduce(sumUp);
    //SOCKET COMMANDS -----------------------------------------
    
    useEffect(() => {
        if (Object.keys(gameData).length === 0) {
            console.log("This should only run on refresh")
            fetch("/checkSession")
            .then(r => r.json())
            .then(data => {
                // restoreGameData(data["user"], data["room"])
                console.log("We are re initializing state")
                console.log(data)
                restoreGameData(data)
                // socket.emit('join_room', {"user": data["user"], "room": data["room"]});
                //Must add failed condition if session brings back nothing...
            })
        } else {
            console.log("joining the rooom......")
            console.log("Has the game data been filled?")
            console.log(gameData)
            socket.emit('join_room', gameData)
        }
    }, [gameData])

    // useEffect(() => {
    //     socket.on('rejoin_at_bet', (data) => {
    //         console.log("received rejoin at bet")
    //         // console.log(data["game"])
    //         if (gameData["user_id"] === data["userId"]) {
    //             console.log("you have rejoined...")
    //             console.log(data["game"]["host"])
    //             setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"] }))
    //             setDisplayBetting(true)
    //             setTimer(Number(data["time"]))
    //         }
    //     })

    //     socket.on("rejoin_game", (data) => {
    //         if (gameData["user_id"] === data["userId"]) {
    //             console.log("rejoining game at regular in between betting rounds....")
    //             setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"]  }))
    //         }
    //     })


    // }, [gameData, socket])


    useEffect(() => {
        //POINT OF RETURN 3/25
        
        socket.on("starting", startingGame);
        socket.on("add_player", addPlayer);
        socket.on("player_left", playerLeft);
        socket.on("dealing", dealing);
        socket.on("dealing_flop", dealingFlop);
        socket.on("dealing_turn", dealingTurn);
        socket.on("dealing_river", dealingRiver);
        socket.on("take_bet", receivingBet);
        socket.on("returning_winners", returningWinners);
        socket.on("end_betting_round", endBettingRound);
        socket.on("auto_fold", autoFold);
        socket.on("reassign_host", reassignHost);
        socket.on("game_is_full", gameIsFull);
        socket.on("wait_for_players", awaitPlayers);
        socket.on("rebuy", allowRebuyOption)
        socket.on("player_has_rebought", playerRebought)
        socket.on("ending_game", endThisGame)

        socket.on("rejoin_at_bet", rejoinAtBet)
        socket.on("rejoin_game", rejoinGame)

        return () => {
            socket.off("starting", startingGame);
            socket.off("add_player", addPlayer);
            socket.off("player_left", playerLeft);
            socket.off("dealing", dealing);
            socket.off("dealing_flop", dealingFlop);
            socket.off("dealing_turn", dealingTurn);
            socket.off("dealing_river", dealingRiver);
            socket.off("take_bet", receivingBet);
            socket.off("returning_winners", returningWinners);
            socket.off("end_betting_round", endBettingRound);
            socket.off("auto_fold", autoFold);
            socket.off("reassign_host", reassignHost);
            socket.off("game_is_full", gameIsFull);
            socket.off("wait_for_players", awaitPlayers);
            socket.off("rebuy", allowRebuyOption)
            socket.off("player_has_rebought", playerRebought)
            socket.off("ending_game", endThisGame)

            socket.off("rejoin_at bet", rejoinAtBet)
            socket.off("rejoin_game", rejoinGame)

        };

    }, [gameData, socket])


    //CHECKING VISUALS AND DEBUGGING ---------------------------
    // console.log(game["deck"]);
    // console.log(game["player_cards"])
    // console.log(tableCards)
    console.log(game)
    


    //SocketFunctions ------------------------------------------
    const addPlayer = (data) => {
        console.log("This runs twice for some reason?")
        console.log("player is joining game...")
        setGame(prevGame => ({...prevGame, player_data: data["player_data"], all_player_cards: data["all_player_cards"], total_players: data["total_players"]}))
    }

    const startingGame = (data) => {
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
    }

    const playerLeft = (data) => {
        console.log("player left game...")
        setGame(prevGame => ({...prevGame, ...data["game"]}))
    }

    const dealing = (data) => {
        console.log("Socket on dealing received on frontend");
        setGame(prevGame => ({...prevGame, player_data: data["adding_cards"], player_cards_dealt: data["player_cards_dealt"], player_cards_dealing: data["dealing"]}))
    }

    const dealingFlop = (data) => {
        // console.log("THIS IS THE FLOP ON THE FRONT END: ")
        // console.log(data);
        console.log("received deal flop");
        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], flop_dealt: true}))
    }

    const dealingTurn = (data) => {
        console.log("TURN HAS BEEN DEALT SOCKET RECEIVED")
        console.log(game)
        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], turn_dealt: true}))

        // setTableCards(data["table_cards"])
        // setTurnDealt(true)
    }

    const dealingRiver = (data) => {
        // console.log(data)
        console.log("received deal river");
        setGame(prevGame => ({...prevGame, table_cards: data["table_cards"], river_dealt: true}))
    }

    const receivingBet = (data) => {
        if (data["user"] === gameData["user_id"]) {
            console.log("BRUUUUUUUUUUUUUUUUUUUUUUUUUH")
            setGame(prevGame => ({...prevGame, ...data["game_update"], player_cash: data["player_cash"], bet_difference: data["bet_difference"]}))
            setDisplayBetting(true)
            setMyBet(Number(data["bet_difference"]))
            setTimer(Number(data["time"]))
            
            //SHOW THE FORM
            //SET GAME flops bets taken to true
            //Bet difference needed to determine minimum needed to achieve call
        } else {
            console.log("other player is betting receiving prior info...")
            setGame(prevGame => ({...prevGame, ...data["game_update"]}))

            // setOpponentBetting(true)
            // setTimer(Number(data["time"]))
        }
    }

    const returningWinners = (data) => {
        console.log("returning winners")
        console.log(data);
        setGame(prevGame => ({
            ...prevGame, winners: data["winners"],
            ...data["game_update"] 
        }))
    }

    const endBettingRound = (data) => {
        console.log("ending bet round")
        // setDisplayBetting(false)
        setGame(prevGame => ({...prevGame, 
            ...data["game_update"],
            min_all_in: data["game_update"]["min_all_in"],
            pots: data["game_update"]["pots"],
            bets: data["game_update"]["bets"],
            main_pot: data["game_update"]["main_pot"]
        }))
    }

    const autoFold = (data) => {
        if (data["host"] === gameData["user_id"]) {
            // const playerUserName = data["user"]
            // const playerId = data["userId"]
            socket.emit("handle_bet_action", {room: gameData["room"], user: data["user"], userId: data["userId"], bet_status: "fold", bet: 0})
        }
    }

    const reassignHost = (data) => {
        console.log("Host reassigned...")
        console.log(data)
        setGame(prevGame => ({...prevGame, host: data["new_host"]}))
    }


    const gameIsFull = (data) => {
        history.push("/");
        alert("GAME WAS FULL")
    }

    const awaitPlayers = (data) => {
        setGame(prevGame => ({...prevGame, ...data}))
    }

    const allowRebuyOption = (data) => {
        console.log("received rebuy option")
        setShowRebuy(true)
    }

    const playerRebought = (data) => {
        // if (data["user_id"] === gameData["user_id"]) {
        //     setShowRebuy(false)
        // }
        console.log("some player rebought...")
        setGame(prevGame => ({...prevGame, player_data: data["player_data"]}))
    }
    
    const endThisGame = (data) => {
        console.log("received end this game")
        console.log(data["game_end"])
        setGame(prevGame => ({...prevGame, "game_over": data["game_end"]}))
    }

    const rejoinAtBet = (data) => {
        // console.log(data["game"])
        console.log("rejoin at bet ran but did not make it...")
        if (gameData["user_id"] === data["user"]) {
            console.log("received rejoin at bet")
            console.log("you have rejoined...")
            console.log(data["game"]["host"])
            setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"] }))
            setDisplayBetting(true)
            setTimer(Number(data["time"]))
        }
    }

    const rejoinGame = (data) => {
        console.log("rejoin at game ran but did not make it...")
        console.log(data);
        if (gameData["user_id"] === data["user"]) {
            console.log("rejoining game at regular in between betting rounds....")
            setGame(prevGame => ({...prevGame, ...data["game"], player_cash: Number(data["player_cash"]), bet_difference: data["bet_difference"]  }))
        }
    }
    //Game FUNCTIONS ------------------------------------------------
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
            //     { name: "A", suit: "Hearts", value: 1, image: "https://deckofcardsapi.com/static/img/AH.png" },
            //     { name: "K", suit: "Hearts", value: 13, image: "https://deckofcardsapi.com/static/img/KH.png"},

            //     { name: "A", suit: "Spades", value: 1, image: "https://deckofcardsapi.com/static/img/AS.png" },
            //     { name: "3", suit: "Diamonds", value: 3, image: "https://deckofcardsapi.com/static/img/3D.png" },
                
            //     { name: "7", suit: "Clubs", value: 7, image: "https://deckofcardsapi.com/static/img/7C.png" },

            //     { name: "8", suit: "Diamonds", value: 8, image: "https://deckofcardsapi.com/static/img/8D.png"  },
            //     { name: "7", suit: "Hearts", value: 7, image: "https://deckofcardsapi.com/static/img/7H.png" },
            //     { name: "J", suit: "Spades", value: 11, image: "https://deckofcardsapi.com/static/img/JS.png" },
                
            //     { name: "7", suit: "Spades", value: 7, image: "https://deckofcardsapi.com/static/img/7S.png" },

            //     { name: "6", suit: "Spades", value: 6, image: "https://deckofcardsapi.com/static/img/6S.png" },
                
            //     { name: "5", suit: "Hearts", value: 5, image: "https://deckofcardsapi.com/static/img/5H.png" },

            //     { name: "5", suit: "Diamonds", value: 5, image: "https://deckofcardsapi.com/static/img/5D.png" },
            //     //Change king back to spade
            //     { name: "3", suit: "Clubs", value: 3, image: "https://deckofcardsapi.com/static/img/3C.png" },
            //     { name: "2", suit: "Hearts", value: 2 },
            //     { name: "3", suit: "Hearts", value: 3 },
            //     { name: "4", suit: "Hearts", value: 4 },
            //     { name: "Q", suit: "Spades", value: 12 },
            //     { name: "6", suit: "Hearts", value: 6 },
            //     { name: "4", suit: "Spades", value: 4, image: "https://deckofcardsapi.com/static/img/4S.png" },
            //     { name: "8", suit: "Hearts", value: 8 },
            //     { name: "9", suit: "Hearts", value: 9 },
            //     { name: "2", suit: "Spades", value: 2 },
            //     { name: "J", suit: "Hearts", value: 11 },
            //     { name: "Q", suit: "Hearts", value: 12 },
            //     { name: "K", suit: "Spades", value: 13, image: "https://deckofcardsapi.com/static/img/KS.png" },

            //     { name: "10", suit: "Hearts", value: 10, image: "https://deckofcardsapi.com/static/img/0H.png" },
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
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["username"], userId: gameData["user_id"], bet_status: status, bet: myBet })
        setDisplayBetting(false)
    }

    function handleCallButton() {
        if (game["min_bet"] !== 0) {
            setDisplayBetting(false)
            socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["username"], userId: gameData["user_id"], bet_status: "call", bet: game["bet_difference"] })
        }
    }

    function handleFoldButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["username"], userId: gameData["user_id"], bet_status: "fold", bet: 0})
        setDisplayBetting(false)
    }
    //Changed bet from bet: game["player_data"][gameData["user"]]["cash"] to game["player_cash"]...check if this leads to issues
    function handleAllInButton() {
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["username"], userId: gameData["user_id"], bet_status: "all_in", bet: game["player_cash"]})
        setDisplayBetting(false)
    }

    function handleCheckButton() {
        setDisplayBetting(false)
        socket.emit("handle_bet_action", {room: gameData["room"], user: gameData["username"], userId: gameData["user_id"], bet_status: "check", bet: 0})
    }

    function run_auto_fold(playerName) {
        console.log("is this running twice? This is auto fold...")
        socket.emit("handle_bet_action", {room: gameData["room"], user: playerName, bet_status: "fold", bet: 0});
    }

    function handleRebuyButton() {
        socket.emit("handle_rebuy", {room: gameData["room"], userId: gameData["user_id"]})
        setShowRebuy(false);
    }




    const handlePopState = () => {
        console.log("hps ran!");
        // socket.emit("back_buttton", {message: "hello"});
        socket.emit("back_button", {})
    }

    // window.onpopstate = () => {
    //     socket.emit("back_buttton", {message: "hello"});
    // }

    //NEW 3/7

    useEffect(() => {
        console.log("USE EFFECT for timer RUNS")
        let updateTimer;
        if (displayBetting === true) {
            console.log(timer)
            if (timer === 0) {
                handleFoldButton();
                // console.log("OUT OF TIME!")
            } else {
                updateTimer = setTimeout(() => {
                    setTimer(prevTimer => prevTimer - 1);
                }, 1000);
            }
            // Clear the timer when displayBetting becomes false
        } 
        // else if (displayBetting === false && opponentBetting === true) {
        //     // let updateTimer;
        //     console.log(timer)
        //     if (timer === 0) {
        //         setOpponentBetting(false);
        //     } else {
        //         updateTimer = setTimeout(() => {
        //             setTimer(prevTimer => prevTimer - 1);
        //         }, 1000);
        //     }
        //     // return () => clearTimeout(updateTimer);
        // }

        return () => clearTimeout(updateTimer);
    }, [timer, displayBetting])


    useEffect(() => {
        console.log("History changed...")
        const listener = history.listen((location, action) => {
            if (action === "POP") {
                handlePopState();
            } else if (action === "PUSH") {
                console.log("Too many players")
            }
        });
        return () => listener();
    }, [history])

    function shuffleAndRestart() {
        console.log("emitting restart....")
        // console.log("fetching new deck and emitting restart...")
            // fetch("/cards")
            // .then(res => res.json())
            // .then(cards => {
            //     //Fisher-Yates alorith
            //     console.log(cards)
            //     for (let i = cards.length - 1; i > 0; i--) {
            //         const j = Math.floor(Math.random() * (i + 1));
            //         const temp = cards[i];
            //         cards[i] = cards[j];
            //         cards[j] = temp;
            //     }
            //     //May need to make shuffle deck into a function for later on
            //     // socket.emit("shuffleDeck", {deck: cards, room: gameData["room"]} );
                
            //     socket.emit('restart_the_game', {deck: cards, room: gameData["room"]});
            // })
            socket.emit('restart_the_game', {room: gameData["room"]});
            
    }

    //GAME LOGIC -------------------------------------------------
    function sayHi() {
        console.log("Hi1")
    }
    
    if (game["game_started"] && game["host"] === gameData["user_id"]) {
        // PLAYER CARDS DEALING
        if (!game["player_cards_dealt"] && !game["player_cards_dealing"]) {
            console.log("going to run deal cards")
            dealPlayerCards(1)
        }
        // PRE GAME BETTING ROUND
        if (!game["pregame_bets_taken"] && game["player_cards_dealt"]) {
            console.log("going to run allow preflop betting")
            // setTimeout(takeBets, 1000)
            takeBets()
        }
        // // FLOP DEALING
        if (!game["flop_dealt"] && game["player_cards_dealt"] && game["pregame_bets_completed"]) {
            console.log("going to run deal flop")
            dealFlop()
        }
        // FLOP BETTING ROUND
        if (!game["flop_bets_taken"] && game["flop_dealt"]) {
            console.log("going to allow post flop betting")
            // setTimeout(takeBets, 1000)
            takeBets()
        }
        // TURN DEALING
        if (!game["turn_dealt"] && game["flop_dealt"] && game["flop_bets_completed"]) {
            console.log("going to run deal turn")
            //WHY DOES THIS RUN TWICE AND WHY IS STATE RESETING???
            setTimeout(dealTurn, 2000)
            // dealTurn()
        }
        // TURN BETTING ROUND
        if (!game["turn_bets_taken"] && game["turn_dealt"]) {
            console.log("going to allow post turn betting")
            // setTimeout(takeBets, 1000)
            takeBets()
        }
        // RIVER DEALING
        if (!game["river_dealt"] && game["turn_dealt"] && game["turn_bets_completed"]) {
            console.log("going to run deal river")
            setTimeout(dealRiver, 2000)
            // dealRiver()
        }
        // RIVER DEALING ROUND
        if (!game["river_bets_taken"] && game["river_dealt"]) {
            console.log("allowing post river betting")
            // setTimeout(takeBets, 1000)
            takeBets()
        }
        if (!game["winners_declared"] && game["player_cards"] && game["flop_dealt"] && game["river_dealt"] && game["river_bets_completed"]) {
            console.log("checking win")
            checkWin()
        }
        if (game["winners_declared"] && !game["game_over"]) {
            console.log("running shuffle and restart....")
            // console.log(game)
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

    
    const displayAllPlayerCards = game["all_player_cards"].map((player) => {
        const playerData = game["player_data"][player];
        const playerId = playerData["userId"];
        const playerName = playerData["user"];
        const currCash = playerData["cash"];
        const currStatus = playerData["status"];

        const playerIcon = playerData["image_icon"];

        let card1 = playerData["cards"][0]["image"];
        let card2 = playerData["cards"][1]["image"];
        const showCards = playerData["showCards"];

        //Need another variable to be false that way at somepoint we can switch to true and show opponents cards
        if (card1 && card2 && (playerId !== gameData["user_id"]) && !showCards) {
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

        //https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/dog-poker-player-cards-cigar-casio-gambler-gift-thomas-larch.jpg
        return (
            <div id={player}>
                {playerId? (
                <>
                {playerTurn? ( 
                <>
                <div id={player + "icon"} style={{boxShadow: "0 0 0 4px rgb(216, 214, 214), 0 0 0 10px rgb(30, 5, 88), 0 0 10px 20px rgba(255, 255, 255, 0.596)"}}>
                    <img id = {player + "img"} src={playerIcon}/>
                </div>
                <div id={player + "info"} style={{border: ".12em solid green"}}>
                    <div className="playerInfoNames">
                        {playerName}
                    </div>
                    {/* <hr/> */}
                    <div className="Money">Cash: ${currCash}</div>
                    <div>Last Bet: </div>         
                </div>
                <div id={player + "tag"}>POKER PRO</div>
                <div id={player + "Emote"}>
                    <img className="emote" src="https://media.tenor.com/GmU85epf9D4AAAAM/pepe-nervous.gif" alt="playerEmote"/>
                </div>
                </>
                ):
                (
                <>
                <div id={player + "icon"}>
                    <img id = {player + "img"} src={playerIcon}/>
                </div>
                <div id={player + "info"} >
                    <div className="playerInfoNames">
                        {playerName}
                    </div>
                    {/* <hr/> */}
                    <div className="Money">Cash: ${currCash}</div>
                    <div>Last Bet: </div>         
                </div>
                <div id={player + "tag"}>POKER PRO</div>
                <div id={player + "Emote"}>
                    <img className="emote" src="https://media.tenor.com/HFhrPAPvytYAAAAM/monka-walk-away-monka-s.gif" alt="playerEmote"/>
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
        // console.log("THIS IS THE INDEX : " + index)
        
        let winnerdinner = ""

        for (let i = 0; i < game["winners"][index].length; i++) {
            winnerdinner += game["player_data"][game["winners"][index][i]]["user"] + " "
        }

        return (<div style={{color: "red", fontSize: "large"}}>
            <div>{index === game["winners"].length - 1 ? "main pot " : "side pot " + parseInt(index + 1)} : {winnerdinner}</div>
        </div>)
    })

    // game["player_ids"].length
    return (
        <div id="fullGamePage">
        <div className="menuBar">
            <div id="exitGame">Leave Room</div>
            <div id="playerCount">Total Players:  {game["total_players"]} / 6</div>
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
                <div id="chipsTray">
                    <div id="innerTray">
                        <div id="chipsInTray1"></div>
                        <div id="chipsInTray2"></div>
                        <div id="chipsInTray3"></div>
                        <div id="chipsInTray4"></div>
                        <div id="chipsInTray5"></div>
                    </div>
                </div>
                <div  id="dealerBox" >
                    <div id="theDealer">
                        <img src={luigi} alt="dealer"/>
                    </div>
                </div>
                
                <div className="icon">
                    
                    <div id="pokerLogoContainer">
                        <img id="pokerLogo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/World_Series_of_Poker_logo.svg/480px-World_Series_of_Poker_logo.svg.png" alt="pokerTableLogo" />
                    </div>
                    <div id="newTableCards">
                        {displayTableCards}
                    </div>
                    {displayAllPlayerCards}
                </div>
                {game["pot"]>= 0? 
                (<div id="potAmount">
                    <div id="tableChips" style={{color: "white"}}>
                        <img src={tableChips} alt="tableChips"/>
                    </div>
                    <div id="potSize">Pot Size: ${game["pot"]}</div>
                    <div>Test Pot: ${game["total_pot"]}</div>
                </div>)
                : 
                (<></>)}
                {game["game_started"]? (<button>End Game</button>): (<div className="startButtonContainer"><button className="startButton" onClick={startGame}>Start Game</button></div>)}
                <div id="betBoxBorder">
                <div id="slotButton1"></div>
                <div id="slots">
                    <div className="slotSevens">
                        <img src="https://cdn3.iconfinder.com/data/icons/casino/256/Cherries-512.png" alt="cherry"/>
                    </div>
                    <div className="slotSevens">
                        <img src="https://cdn3.iconfinder.com/data/icons/casino/256/Cherries-512.png" alt="cherry"/>
                    </div>
                    <div className="slotSevens">
                        <img src="https://cdn3.iconfinder.com/data/icons/casino/256/Cherries-512.png" alt="cherry"/>
                    </div>
                </div>
                <div id="slotButton2"></div>
                <div id="betBox" style={{"--c": "5px solid blue"}}>
                    {/* {displayAllPlayerCards} */}
                    {showRebuy? (<button onClick={handleRebuyButton}>REBUY</button>): (<></>)}
                    {displayBetting ?
                    (
                    <div id="betDisplay">
                        <form id="betForm" onSubmit={handleBetSubmit}>
                            <label>Bet Amount:</label>
                            <input type="number" min={game["bet_difference"]} max = {game["player_cash"]} value = {myBet} onChange={handleBetChange}/>
                            <div id="betButtonBorder">
                                <button id="betButton" type="submit">Bet</button>
                            </div>
                        </form>
                        <div id="otherBetButtons">
                            {game["bet_difference"] === 0? <div id="checkButtonBorder"><button id="checkButton" onClick={handleCheckButton}>CHECK</button></div>: <></>}
                            {game["bet_difference"] > 0? <div id="callButtonBorder"><button id="callButton" onClick={handleCallButton}>{"CALL" + " $" + game["bet_difference"]}</button></div> : <></> }
                            <div id="allInButtonBorder">
                                <button id="allInButton" onClick={handleAllInButton}>ALL IN</button>
                            </div>
                            <div id="foldButtonBorder">
                                <button id="foldButton" onClick={handleFoldButton}>FOLD</button>
                            </div>
                            
                            
                        </div>

                  
                        
                    </div>):
                    (<></>)
                    }
                    {winnersDisplay}

                    
                </div>
                </div>
            </div>
                <div id="timer">
                    <div id="timerTime">
                        {timer >= 10? (<>{`00:${timer}`}</>): (<>{`00:0${timer}`}</>)}
                    </div>
                </div>
        </div>
        </div>
        </div>
    )
}

export default Game