import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom/cjs/react-router-dom.min";
import Header from "./Header";

function Homepage({fillGameData, loggedInUser}) {
    return (
    <>
        <Header loggedInUser={loggedInUser}></Header>
    </>
    )
}

export default Homepage