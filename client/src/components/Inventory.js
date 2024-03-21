import React, { useEffect, useState } from "react";

function Inventory() {
    const [icons, setIcons] = useState([])
    const [tags, setTags] = useState([])
    const [condition, setCondition] = useState(false)

    useEffect(() => {
        fetch("/usericons/1")
        .then(response => response.json())
        .then(userIconData => {
            console.log(userIconData)
            setIcons(userIconData)
            fetch("/usertags/1")
            .then(response => response.json())
            .then(userTagData => {
                console.log(userTagData)
                setTags(userTagData)
            })
        })
    }, [])


    console.log("bruh")
    const iconsDisplay = icons.map((icon) => {
        return <div key={icon.id}>
            <h2>{icon["icon"]["name"]}</h2>
            <img src={icon["icon"]["content"]} style={{ width: '250px', height: '250px' }} ></img>
        </div>
    })

    const tagsDisplay = tags.map((tag) => {
        return <div key={tag.id}>
            <h3>{tag["tag"]["name"]}</h3>
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