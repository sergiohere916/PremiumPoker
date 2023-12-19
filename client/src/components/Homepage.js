import React from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";


function Homepage() {


    return (
    <div>
        <NavLink to="/game"><button>Start A Game</button></NavLink>
    </div>)
}

export default Homepage