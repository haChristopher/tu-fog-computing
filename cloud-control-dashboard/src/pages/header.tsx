import { Typography } from "@mui/material";
import "chartjs-adapter-date-fns";
import "../App.css";
import LogoTU from "../images/tu-berlin-logo-long-red.svg 17-34-37-272.svg";

export default function Header() {
  return (
    <>
      <div className="header">
        <img className="logo" alt="Logo TU Berlin" src={LogoTU} />
        <Typography variant="h4" align="center" sx={{ color: "white" }}>
          Weather Station
        </Typography>
      </div>
    </>
  );
}
