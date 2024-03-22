import React, { useEffect, useState } from "react";

function Shop({userIcons, userTags, loggedInUser, onLogin}) {
    console.log("THIS IS RE-RENDERED USER")
    console.log(loggedInUser)
    console.log("BRUUUUUUUUUUUUUUH RERENDER ON SHOPPPPPPPPPPPPPP")
    const [icons, setIcons] = useState([])
    const [tags, setTags] = useState([])
    const [condition, setCondition] = useState(false)

    useEffect(() => {
        console.log("IS THIS USE EFFECT RUNNING???")
        fetch("/icons")
        .then(response => response.json())
        .then(iconData => {
            setIcons(iconData)
            fetch("/tags")
            .then(response => response.json())
            .then(tagData => {
                setTags(tagData)
            })
        })
    }, [])

    function purchaseIcon(e) {
        // Checking if the price matches the user's points
        if (loggedInUser["points"] >= e["price"]) {
            // Updating the points on the backend
            // I'm patching the points
            // Im not sure why Shop is not re-rendering when we reset the User
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({"points" : loggedInUser["points"] - e["price"]})
            })
            .then(response => response.json())
            .then(userData => {
                // Creating new association table between user and icon
                fetch("/usericons", {
                    method : "POST",
                    headers : {"Content-Type" : "application/json"},
                    body : JSON.stringify({user_id : loggedInUser["id"], icon_id : e["id"]})
                })
                .then(response => response.json())
                .then(data => {
                    onLogin({...loggedInUser, userData})
                })
            })
        }
    }

    function purchaseTag(e) {
        if (loggedInUser["points"] >= e["price"]) {
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({"points" : loggedInUser["points"] - e["price"]})
            })
            .then(response => response.json())
            .then(userData => {
                fetch("/usertags", {
                    method : "POST",
                    headers : {"Content-Type" : "application/json"},
                    body : JSON.stringify({user_id : loggedInUser["id"], tag_id : e["id"]})
                })
                .then(response => response.json())
                .then(data => {
                    onLogin({...loggedInUser, userData})
                })
            })
        }
    }

    
    // Im mapping through usericons and usertags to just get the names only
    // I think this might be the issue yeah
    const userIconNames = userIcons.map(icon => icon.name);
    const userTagNames = userTags.map(tag => tag.name)

    const iconsDisplay = icons.map((icon) => {
        return (
            <div key={icon.content}>
                <h2>{icon.name}</h2>
                <img 
                    src={icon.content} 
                    style={{ width: '250px', height: '250px' }} 
                    alt={`Icon ${icon.content}`} 
                />
                <h3 style={{ background : "white"}}>Price : {icon.price}</h3>
                {/* And then in here, I just check if that icon name is inside the array, and if it is, that means its in the inventory */}
                <button onClick={() => userIconNames.includes(icon["name"]) ? null : purchaseIcon(icon)}>{userIconNames.includes(icon["name"]) ? "OWNED" : "BUY"}</button>
            </div>
        );
    });

    const tagsDisplay = tags.map((tag) => {
        return (
            <div key={tag.name}>
                <h2>{tag.name}</h2>
                <h3>Price : {tag.price}</h3>
                <button onClick={() => userTagNames.includes(tag["name"]) ? null : purchaseTag(tag)}>{userTagNames.includes(tag["name"]) ? "OWNED" : "BUY"}</button>
            </div>
        )
    })
    
    function handleButton(e) {
        setCondition(!condition)
    }

    return (<div>
        <button onClick={handleButton}>{condition ? "icons" : "tags"}</button>
        <div>
            {condition ? tagsDisplay : iconsDisplay}
        </div>
    </div>)
}

export default Shop