import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";

function Profile() {
    const {id} = useParams()
    const [userObj, setUserObj] = useState({})

    useEffect(() => {
        fetch(`/users/${id}`)
        .then(response => response.json())
        .then(data => {
            setUserObj(data)
        })
    })

    return (
        <div id="profile-container">
            <div id="top-profile-section">
                <img id="profile-image"src={userObj["image_url"]}></img>
                <h1 id="username-display">{userObj["username"]}</h1>
            </div>
            <div id="bottom-profile-section">
                <h2 id="user-tag">{userObj["tag"] == "" ? "None" : }</h2>
                <div id="points">POINTS : {userObj["points"]}</div>
                <div id="total-points">TOTAL POINTS : {userObj["total_points"]}</div>
            </div>
        </div>
    )
        
}

export default Profile


