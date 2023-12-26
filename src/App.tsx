import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Sidebar, Menu, MenuItem, SubMenu } from "react-pro-sidebar";
import { Link } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Sidebar>
        <Menu>
          Charles Young
          <MenuItem>Home</MenuItem>
          <MenuItem>About</MenuItem>
          <MenuItem>Tags</MenuItem>
        </Menu>
      </Sidebar>
    </div>
  );
}

export default App;
