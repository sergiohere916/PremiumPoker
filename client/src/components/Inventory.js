import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Inventory({userIcons, userTags, loggedInUser, onLogin}) {
    const [condition, setCondition] = useState(false)
    const history = useHistory()

    console.log(userIcons)
    console.log(userTags)

    function handleBack() {
        history.push("/")
    }

    function handleClickIcon(e, chosenIcon) {
        if (chosenIcon["content"] !== loggedInUser["image_url"]) {
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({image_url : chosenIcon["content"]})
            })
            .then(response => response.json())
            .then(data => {
                e["target"]["textContent"] = "USING"
                onLogin(data)
            })
        }
    }

    function handleClickTag(e, chosenTag) {
        if (chosenTag["name"] !== loggedInUser["tag"]) {
            fetch(`/users/${loggedInUser["id"]}`, {
                method : "PATCH",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({tag : chosenTag["name"]})
            })
            .then(response => response.json())
            .then(data => {
                e["target"]["textContent"] = "USING"
                onLogin(data)
            })
        }
    }

    const iconsDisplay = userIcons.map((icon) => {
        return <div key={icon.id} className="icon-container">
            <h2>{icon["name"]}</h2>
            <img src={icon["content"]} style={{ width: '250px', height: '250px' }} ></img>
            <button className="itemButton" onClick={(e) => handleClickIcon(e, icon)}>{icon["content"] == loggedInUser["image_url"] ? "USING" : "USE"}</button>
        </div>
    })

    const tagsDisplay = userTags.map((tag) => {
        return <div key={tag.id} className="tag-container">
            <h3>{tag["name"]}</h3>
            <button className="itemButton" onClick={(e) => handleClickTag(e, tag)}>{tag["name"] == loggedInUser["tag"] ? "USING" : "USE"}</button>
        </div>
    })

    function handleButton(e) {
        setCondition(!condition)
    }

    return (<div id="shop-container">
        <button onClick={handleBack} id="back-button">BACK</button>
        <div id="inventory">
            <h3 className="heading-title">INVENTORY</h3>
            <button id="toggle-button" onClick={handleButton}>{condition ? "tags" : "icons"}</button>
            <div id="items-display">
                {condition ? iconsDisplay : tagsDisplay}
            </div>
        </div>
        
    </div>)
}

export default Inventory