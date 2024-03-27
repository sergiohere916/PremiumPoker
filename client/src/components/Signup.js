import React, { useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Signup({onLogin}) {

    const history = useHistory()
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
                    onLogin(userData)
                    setUser(initial)
                    history.push("/")
                })
            }
        })
    }

    function handleLoginClick() {
        history.push("/login")
    }

    function handleChange(e) {
        const {name, value} = e.target

        setUser({
            ...user,
            [name] : value
        })
    }

    return (<div id="form-container">
        <form id="form" onSubmit={handleSubmit}>
            <div id="form-header">
                <h2>SIGN UP</h2>
            </div>
            <div className="input-container" id="username-input-container">
                <input
                className="inputs"
                type="text"
                name="username"
                autoComplete="off"
                value={user.username}
                placeholder="username"
                onChange={handleChange}
                ></input>
            </div>
            <div className="input-container" id="password-input-container">
                <input
                    className="inputs"
                    type="password"
                    name="password"
                    value={user.password}
                    placeholder="password"
                    onChange={handleChange}
                >
                </input>
            </div>
            <div className="input-container" id="password-confirmation-container">
                <input
                    className="inputs"
                    type="password"
                    name="passwordConfirmation"
                    value={user.passwordConfirmation}
                    onChange={handleChange}
                    placeholder="password confirm"
                ></input>
            </div>
            <input type="submit" value="Sign up"></input>
            <div id="already">Already have an account? <span onClick={handleLoginClick}>Login</span></div>
        </form>
    </div>)
}

export default Signup