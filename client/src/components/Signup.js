import React, { useState } from "react";

function Signup() {
    const initial = {
        username : "",
        password :  "",
        passwordConfirmation : ""
    }

    const [user, setUser] = useState(initial)

    function handleSubmit(e) {
        e.preventDefault()
        
        fetch("/signup", {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify(user)
        })
        .then((response) => {
            if (response.ok) {
                response.json().then((userData) => {
                    console.log(userData)
                    setUser(initial)
                })
            }
        })
    }

    function handleChange(e) {
        const {name, value} = e.target

        setUser({
            ...user,
            [name] : value
        })
    }

    return (<div>
        <form onSubmit={handleSubmit}>
            <h3>Sign up</h3>
            <input
                type="text"
                name="username"
                autoComplete="off"
                value={user.username}
                placeholder="username"
                onChange={handleChange}
            ></input>
            <input
                type="password"
                name="password"
                value={user.password}
                placeholder="password"
                onChange={handleChange}
            >
            </input>
            <input
                type="password"
                name="passwordConfirmation"
                value={user.passwordConfirmation}
                onChange={handleChange}
                placeholder="password confirm"
            ></input>
            <input type="submit" value="Sign Up"></input>
        </form>
    </div>)
}

export default Signup