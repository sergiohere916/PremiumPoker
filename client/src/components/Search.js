import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Search() {
    const history = useHistory()

    const [allPlayers, setAllPlayers] = useState([])
    const [searchTerm, setSearchTerm] = useState("")

    function handleChange(event) {
        setSearchTerm(event.target.value);
    }

    useEffect(() => {
        fetch("/users")
        .then(response => response.json())
        .then(data => {
            setAllPlayers(data)
        })
    }, [])

    const playersToDisplay = allPlayers.filter((player) =>
        player.username.toLowerCase().includes(searchTerm.toLowerCase())
    );

    function handleClickProfile(user) {
        history.push(`/user/${user.id}`)
    }

    const displayPlayers = playersToDisplay.map((player) => {
        return <div key={player.username} class="player-profile-container" onClick={() => handleClickProfile(player)}>
            <img className="player-icon" src={player.image_url} alt="image"></img>
            <div className="username-tag-container">
                <div className="player-username">{player.username}</div>
                <div className="player-tag">{player.tag == "" ? "None" : player.tag}</div>
            </div>
        </div>
    })

    console.log(allPlayers)

    return (<div id="search-container">
        <h1 id="search-header">SEARCH PLAYERS</h1>
        <input id="search-bar" value={searchTerm} type="search" onChange={handleChange} placeholder="search username..."/>
        <div id="divider"></div>
        <div id="display-players-container">
            {displayPlayers}
        </div>
        
    </div>)
}

export default Search