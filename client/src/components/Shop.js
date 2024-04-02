import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Shop({userIcons, userTags, loggedInUser, onLogin, addNewUserIcon, addNewUserTag}) {
    const [icons, setIcons] = useState([])
    const [tags, setTags] = useState([])
    const [condition, setCondition] = useState(false)
    const [userIconNames, setUserIconNames] = useState([]);
    const [userTagNames, setUserTagNames] = useState([]);

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

    
    // Im mapping through usericons and usertags to just get the names only
    // I think this might be the issue yeah
    useEffect(() => {
        const iconNames = userIcons.map(icon => icon.name);
        const tagNames = userTags.map(tag => tag.name);
        setUserIconNames(iconNames);
        setUserTagNames(tagNames);
    }, [userIcons, userTags]);

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
                <h3 class="price">Price : {tag.price} Premium points</h3>
                <button className="itemButton" onClick={(e) => userTagNames.includes(tag["name"]) ? null : purchaseTag(e, tag)}>{userTagNames.includes(tag["name"]) ? "OWNED" : "BUY"}</button>
            </div>
        )
    })
    
    function handleButton(e) {
        setCondition(!condition)
    }
    
    function handleBack() {
        history.push("/")
    }

    return (
    <div id="shop-container">
        <button onClick={handleBack} id="back-button">BACK</button>
        <div id="shop">
            <h3 className="heading-title">SHOP</h3>
            <button id="toggle-button" onClick={handleButton}>{condition ? "ICONS" : "TAGS"}</button>
            <div id="featuredBar">Featured Items</div>
            <div id="items-display">
                {condition ? tagsDisplay : iconsDisplay}
            </div>
        </div>
    </div>)
    
}

export default Shop