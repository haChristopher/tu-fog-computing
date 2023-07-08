import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WindSpeed from "./pages/wind_speed";
import Temperature from "./pages/temperature";
import Humidity from "./pages/humidity";
import Pressure from "./pages/pressure";
import Header from "./pages/header";
import "./App.css";

function App() {
  return (
    <>
      <Header />
      <div className="container">
        <Temperature />
        <WindSpeed />
        <Humidity />
        <Pressure />
      </div>
    </>
  );
}

export default App;
