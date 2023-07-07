import { Component } from "react";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import "./home.css";
import Temperature from "./temperature";

export default function Buttons() {
  return (
    <>
      <div className="header">
        <div className="text">
          <Typography variant="h5">Weather Station Dashboard</Typography>
        </div>
        <div className="buttons">
          <Button variant="outlined">Weather Station Berlin</Button>
          <Button variant="outlined">Weather Station Hamburg</Button>
          <Button variant="outlined">Weather Station München</Button>
        </div>
      </div>
    </>
  );
}
