import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Shop({userIcons, userTags, userEmotes, loggedInUser, onLogin, addNewUserIcon, addNewUserTag, addNewUserEmote}) {
    const [icons, setIcons] = useState([])
    const [tags, setTags] = useState([])
    const [emotes, setEmotes] = useState([])
    const [condition, setCondition] = useState("")
    const [userIconNames, setUserIconNames] = useState([]);
    const [userTagNames, setUserTagNames] = useState([]);
    const [userEmoteNames, setUserEmoteNames] = useState([]);

    const history = useHistory()

    useEffect(() => {
        fetch("/icons")
        .then(response => response.json())
        .then(iconData => {
            setIcons(iconData)
            fetch("/tags")
            .then(response => response.json())
            .then(tagData => {
                setTags(tagData)
                fetch("/emotes")
                .then(response => response.json())
                .then(emoteData => {
                    setEmotes(emoteData)
                })
            })
        })
    }, [])

    function purchaseIcon(e, icon) {
        if (loggedInUser["points"] >= icon["price"]) {
            // Updating the points on the backend
            // I'm patching the points
            // Im not sure why Shop is not re-rendering when we reset the User
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({"points" : loggedInUser["points"] - icon["price"]})
            })
            .then(response => response.json())
            .then(userData => {
                // Creating new association table between user and icon
                fetch("/usericons", {
                    method : "POST",
                    headers : {"Content-Type" : "application/json"},
                    body : JSON.stringify({user_id : loggedInUser["id"], icon_id : icon["id"]})
                })
                .then(response => response.json())
                .then(data => {
                    // console.log(data)
                    e.target.textContent = "OWNED"
                    // onLogin(userData)
                    addNewUserIcon(data)
                })
            })
        }
    }

    function purchaseTag(e, tag) {
        if (loggedInUser["points"] >= tag["price"]) {
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({"points" : loggedInUser["points"] - tag["price"]})
            })
            .then(response => response.json())
            .then(userData => {
                fetch("/usertags", {
                    method : "POST",
                    headers : {"Content-Type" : "application/json"},
                    body : JSON.stringify({user_id : loggedInUser["id"], tag_id : tag["id"]})
                })
                .then(response => response.json())
                .then(data => {
                    e.target.textContent = "OWNED"
                    // onLogin(userData)
                    addNewUserTag(data)
                })
            })
        }
    }

    function purchaseEmote(e, emote) {
        if (loggedInUser["points"] >= emote["price"]) {
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({"points" : loggedInUser["points"] - emote["price"]})
            })
            .then(response => response.json())
            .then(userData => {
                // Creating new association table between user and emote
                fetch("/useremotes", {
                    method : "POST",
                    headers : {"Content-Type" : "application/json"},
                    body : JSON.stringify({user_id : loggedInUser["id"], emote_id : emote["id"]})
                })
                .then(response => response.json())
                .then(data => {
                    // console.log(data)
                    e.target.textContent = "OWNED"
                    // onLogin(userData)
                    addNewUserEmote(data)
                })
            })
        }
    }

    
    // Im mapping through usericons and usertags to just get the names only
    // I think this might be the issue yeah
    useEffect(() => {
        const iconNames = userIcons.map(icon => icon.name);
        const tagNames = userTags.map(tag => tag.name);
        const userEmoteNames = userEmotes.map(emote => emote.name)
        setUserIconNames(iconNames);
        setUserTagNames(tagNames);
        setUserEmoteNames(userEmoteNames)
    }, [userIcons, userTags, userEmotes]);

    const emotesDisplay = emotes.map((emote) => {
        return (
            <div key={emote.content} className="emote-container">
                <h2>{emote.name}</h2>
                <img src={emote.content} style={{ width: '250px', height: '250px' }}></img>
                <h3>Price : {emote.price} Premium points</h3>
 
                <button className="itemButton" onClick={(e) => userEmoteNames.includes(emote["name"]) ? null : purchaseEmote(e, emote)}>{userEmoteNames.includes(emote["name"]) ? 
                <span className="ownedIconLabel">
                    <div>OWNED</div>
                    <div id="ownedIconMark">
                        <img src="https://static.vecteezy.com/system/resources/previews/017/177/781/non_2x/green-tick-check-mark-on-transparent-background-free-png.png"/>
                    </div>
                </span> : "BUY"}

                </button>
            </div>
        )
    })

    const iconsDisplay = icons.map((icon) => {
        return (
            <div key={icon.content} className="icon-container">
                <h2>{icon.name}</h2>
                <img 
                    src={icon.content} 
                    style={{ width: '250px', height: '250px' }} 
                    alt={`Icon ${icon.content}`} 
                />
                <h3>Price : {icon.price} Premium points</h3>
                {/* And then in here, I just check if that icon name is inside the array, and if it is, that means its in the inventory */}
                <button className="itemButton" onClick={(e) => userIconNames.includes(icon["name"]) ? null : purchaseIcon(e, icon)}>{userIconNames.includes(icon["name"]) ? 
                <span className="ownedIconLabel">
                    <div>OWNED</div>
                    <div id="ownedIconMark">
                        <img src="https://static.vecteezy.com/system/resources/previews/017/177/781/non_2x/green-tick-check-mark-on-transparent-background-free-png.png"/>
                    </div>
                </span> : "BUY"}

                </button>
            </div>
        );
    });

    const tagsDisplay = tags.map((tag) => {
        return (
            <div key={tag.name} className="tag-container">
                <h2>{tag.name}</h2>
                <h3 className="price">Price : {tag.price} Premium points</h3>
                <button className="itemButton" onClick={(e) => userTagNames.includes(tag["name"]) ? null : purchaseTag(e, tag)}>{userTagNames.includes(tag["name"]) ? "OWNED" : "BUY"}</button>
            </div>
        )
    })
    
    function handleButton(e) {
        console.log(e)
        setCondition(e.target.textContent)
    }
    
    function handleBack() {
        history.push("/")
    }

    return (
    <div id="shop-container">
        <button onClick={handleBack} id="back-button">BACK</button>
        <div id="shop">
            <h3 className="heading-title">SHOP</h3>
            <div className="buttons-container">
                <button id="toggle-button" onClick={handleButton}>ICONS</button>
                <button id="toggle-button" onClick={handleButton}>TAGS</button>
                <button id="toggle-button" onClick={handleButton}>EMOTES</button>
            </div>
            <div id="featuredBar">Featured Items</div>
            <div id="items-display">
                {condition == "ICONS" ? iconsDisplay : (condition == "TAGS" ? tagsDisplay : emotesDisplay)}
            </div>
        </div>
    </div>)
    
}

export default Shop