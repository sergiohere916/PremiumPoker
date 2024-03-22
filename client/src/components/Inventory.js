import React, { useEffect, useState } from "react";

function Inventory({userIcons, userTags, loggedInUser}) {
    const [condition, setCondition] = useState(false)

    console.log(userIcons)
    console.log(userTags)

    const iconsDisplay = userIcons.map((icon) => {
        return <div key={icon.id}>
            <h2>{icon["name"]}</h2>
            <img src={icon["content"]} style={{ width: '250px', height: '250px' }} ></img>
            <button>USE</button>
        </div>
    })

    const tagsDisplay = userTags.map((tag) => {
        return <div key={tag.id}>
            <h3>{tag["name"]}</h3>
            <button>USE</button>
        </div>
    })

    function handleButton(e) {
        setCondition(!condition)
    }

    return (<div>
        <h1>oiadfosij</h1>
        <button onClick={handleButton}>{condition ? "tags" : "icons"}</button>
        {condition ? iconsDisplay : tagsDisplay}
    </div>)
}

export default Inventory