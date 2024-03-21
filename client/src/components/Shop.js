import React, { useEffect, useState } from "react";

function Shop() {
    const [icons, setIcons] = useState([])
    const [tags, setTags] = useState([])
    const [condition, setCondition] = useState(false)

    useEffect(() => {
        fetch("/icons")
        .then(response => response.json())
        .then(iconData => {
            setIcons(iconData)
            fetch("/tags")
            .then(response => response.json())
            .then(tagData => {
                setTags(tagData)
                console.log(tagData)
                console.log(iconData)
            })
        })
    }, [])

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
                <button>BUY</button>
            </div>
        );
    });

    const tagsDisplay = tags.map((tag) => {
        return (
            <div key={tag.name}>
                <h2>{tag.name}</h2>
                <h3>Price : {tag.price}</h3>
                <button>BUY</button>
            </div>
        )
    })
    
    function handleButton(e) {
        setCondition(!condition)
    }

    console.log(condition)

    return (<div>
        <button onClick={handleButton}>{condition ? "tags" : "icons"}</button>
        <div>
            {condition ? tagsDisplay : iconsDisplay}
        </div>
    </div>)
}

export default Shop