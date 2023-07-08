import { Typography } from "@mui/material";
import "chartjs-adapter-date-fns";
import "./home.css";

export default function Header() {
  return (
    <>
      <div className="header">
        <Typography variant="h5">Weather Station Dashboard</Typography>
      </div>
    </>
  );
}
