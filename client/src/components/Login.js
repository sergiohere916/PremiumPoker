import React, { useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Login({onLogin}) {

    const history = useHistory()

    const initial = {
        username : "",
        password : ""
    }

    const [testUser, setTestUser] = useState(initial)

    function handleSubmit(e) {
        e.preventDefault()

        fetch("/login", {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify(testUser)
        })
        .then((response) => {
            if (response.ok) {
                response.json().then(userData => {
                    onLogin(userData)
                    history.push("/")
                    setTestUser(initial)
                })
            }
        })
    }

    function handleRegisterClick() {
        history.push("/signup")
    }

    function handleChange(e) {
        const {name, value} = e.target
        setTestUser({
            ...testUser,
            [name] : value
        })
    }

    return (<div id="form-container">
        <form id="form" onSubmit={handleSubmit}>
            <div id="form-header">
                <h2>LOGIN</h2>
            </div>
            <div className="input-container">
                <input
                    type="text"
                    name="username"
                    value={testUser.username}
                    onChange={handleChange}
                    placeholder="Username"
                ></input>
            </div>
            <div className="input-container">
                <input
                    type="password"
                    name="password"
                    value={testUser.password}
                    onChange={handleChange}
                    placeholder="Password"
                ></input>
            </div>
            <input type="submit" value="Login"></input>
            <div id="already">Don't have an account? <span onClick={handleRegisterClick}>Register</span></div>
        </form>
    </div>)
}

export default Login