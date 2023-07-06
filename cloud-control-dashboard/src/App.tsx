import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WindSpeed from "./pages/wind_speed";
import Temperature from "./pages/temperature";
import Humidity from "./pages/humidity";
import Pressure from "./pages/pressure";
import Buttons from "./pages/buttons";
import "./App.css";

function App() {
  return (
    <>
      <Buttons />
      <div className="container">
        <Temperature />
        <WindSpeed />
        <Humidity />
        <Pressure />
      </div>
    </>
    // <Router>
    //   <Routes>
    //     <Route path="/" element={<Home />} />
    //     <Route path="/home_right" element={<Home_right />} />
    //   </Routes>
    // </Router>
  );
}

export default App;
