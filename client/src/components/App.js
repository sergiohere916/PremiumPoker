import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Game from "./Game";
import Homepage from "./Homepage";

function App() {
  return (
  <div>
    <Switch>
      <Route path="/game">
        <Game/>
      </Route>
      <Route path="/">
        <Homepage/>
      </Route> 
    </Switch>
  </div>
  )
}

export default App;
