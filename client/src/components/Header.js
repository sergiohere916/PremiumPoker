import React from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";

function Header({loggedInUser, logoutUser}) {

    const selfId = `/user/${loggedInUser["id"]}`

    function handleLogout() {
        fetch("/logout", {
            method: "DELETE"
        })
        .then(response => {
            if (response.ok) {
                logoutUser()
            }
        })
        
    }
    // PREMIUM POKER
    return (
        <div id="header">
            <div id="logo">PREMIUM POKER</div>
            <div id="nav-container">
                
                <NavLink to="/play">PLAY</NavLink>
                <NavLink to="/leaderboard">LEADERBOARD</NavLink>
                <NavLink to="/search">SEARCH</NavLink>
                <NavLink to="/shop">STORE</NavLink>
                {loggedInUser["type"] == "GUEST" ? <NavLink to="/login" >LOGIN</NavLink> : ""}
                {loggedInUser["type"] == "GUEST" ? "" : <NavLink to="/inventory">INVENTORY</NavLink>}
                {loggedInUser["type"] == "GUEST" ? <NavLink to="/signup" >SIGN UP</NavLink> : ""}
                {loggedInUser["type"] == "GUEST" ? "" : <a onClick={handleLogout}>LOGOUT</a>}
                {loggedInUser["type"] == "GUEST" ? "" : <NavLink to={selfId} >PROFILE</NavLink>}
                </div>
        </div>
    )
}

export default Header