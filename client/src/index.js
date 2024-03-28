import React from "react";
import App from "./components/App";
import "./index.css";
import "./css/Homepage.css"
import "./css/Header.css"
import "./css/Signup.css"
import "./css/Shop.css"
import "./css/Inventory.css"
import { createRoot } from "react-dom/client";
import {BrowserRouter} from 'react-router-dom';

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
<BrowserRouter>
    <App />
</BrowserRouter>
);
