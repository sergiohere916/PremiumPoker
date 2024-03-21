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
                    // console.log(userData)
                    onLogin(userData)
                    history.push("/")
                    setTestUser(initial)
                })
            }
        })
    }

    function handleChange(e) {
        const {name, value} = e.target
        setTestUser({
            ...testUser,
            [name] : value
        })
    }

    return (<div>
        <form onSubmit={handleSubmit}>
            <h3>Login</h3>
            <input
                type="text"
                name="username"
                value={testUser.username}
                onChange={handleChange}
                placeholder="Username"
            ></input>
            <input
                type="password"
                name="password"
                value={testUser.password}
                onChange={handleChange}
                placeholder="Password"
            ></input>
            <input type="submit" value="Login"></input>
        </form>
    </div>)
}

export default Login