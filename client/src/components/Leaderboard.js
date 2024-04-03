import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Leaderboard() {
    const history = useHistory()
    const [leaderboardPlayers, setLeaderboardPlayers] = useState([])


    useEffect(() => {
        fetch("/users_points")
        .then(response => response.json())
        .then(data => {
            setLeaderboardPlayers(data)
        })
    })

    function handleClick(player) {
        history.push(`/user/${player.id}`)
    }

    let i = 0

    const displayLeaderboard = leaderboardPlayers.map((player) => {
        i++;
        return <div key={player["id"]} className="playerboard-container" onClick={() => handleClick(player)}>
            <div className="leaderboard-ranking">#{i}</div>
            <img className="leaderboard-icon" src={player["image_url"]} alt="no image"></img>
            <div className="leaderboard-username">{player["username"]}</div>
            <div className="leaderboard-totalpoints">{player["total_points"]}</div>
        </div>
    })

    return (<div id="leaderboard-container">
        <h1 id="leaderboard-header">LEADERBOARD</h1>
        <div id="leaderboard-labels">
            <div>RANK</div>
            <div>ICON</div>
            <div>PLAYER</div>
            <div>POINTS</div>
        </div>
        {displayLeaderboard}
    </div>)
}

export default Leaderboard