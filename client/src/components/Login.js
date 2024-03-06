import React, { useState } from "react";

function Login() {

    const initial = {
        username : "",
        password : ""
    }

    const [user, setUser] = useState(initial)

    function handleChange(e) {
        const {name, value} = e.target
        setUser({
            ...user,
            [name] : value
        })
    }

    return (<div>
        <form>
            <h3>Login</h3>
            <input
                type="text"
                name="username"
                value={user.username}
                onChange={handleChange}
                placeholder="Username"
            ></input>
            <input
                type="password"
                name="password"
                value={user.password}
                onChange={handleChange}
                placeholder="Password"
            ></input>
            <input type="submit" value="Login"></input>
        </form>
    </div>)
}

export default Login