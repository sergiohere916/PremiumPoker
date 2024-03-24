import React from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";

function Header({loggedInUser}) {
    return (
        <>
        <div id="header">
            <div id="logo">PREMIUM POKER</div>
            <div id="nav-container">
                <NavLink to="/play">PLAY</NavLink>
                <NavLink to="/shop">STORE</NavLink>
                {loggedInUser["type"] == "GUEST" ? <NavLink to="/login" >LOGIN</NavLink> : ""}
                {loggedInUser["type"] == "GUEST" ? "" : <NavLink to="/inventory">INVENTORY</NavLink>}
                {loggedInUser["type"] == "GUEST" ? <NavLink to="/signup" >SIGN UP</NavLink> : ""}
            </div>
        </div>
        </>
    )
}

export default Header