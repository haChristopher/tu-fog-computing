import { Component } from "react";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import "./chart.css";

import {
  Chart,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  TimeScale,
  LineController,
  LineElement,
} from "chart.js";
import { isConstructorDeclaration } from "typescript";

Chart.register(
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  TimeScale,
  LineController,
  LineElement
);

interface DataPoint {
  x: string;
  y: number;
}

interface ChartData {
  datasets: {
    label: string;
    data: DataPoint[];
    fill: boolean;
    borderColor: string;
    borderWidth: number;
  }[];
}

interface State {
  chartData: ChartData;
  city: string;
}

class Humidity extends Component<{}, State> {
  private interval: NodeJS.Timeout | null = null;

  constructor(props: any) {
    super(props);

    this.state = {
      chartData: {
        datasets: [
          {
            label: "Humidity",
            data: [],
            fill: false,
            borderColor: "rgba(0, 0, 0, 1)",
            borderWidth: 2,
          },
        ],
      },
      city: "Berlin", // Default city
    };

    this.addHumidityDataPoint = this.addHumidityDataPoint.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addHumidityDataPoint, 1000);
    this.changeCity = this.changeCity.bind(this);
  }

  // hier GET data einbauen
  async getHumidityDataPoint(city: string) {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v2/get_single?city=${city}`
    );
    const data = await response.json();

    let humudityDataArray = [];

    for (let i = 0; i < data.length; i++) {
      // unix timestamp
      let timeMeasurement = data[i].time_of_measurement;
      // convert to date
      let date = new Date(timeMeasurement * 1000).toISOString();

      let temp = data[i].humidity;
      let dataPoint = { x: date, y: temp };
      // console.log(timeMeasurement, date, `Temperature: ${temp}`);

      // unshift will put it at the beginning of the array (order is then correct)
      humudityDataArray.unshift(dataPoint);
    }
    return humudityDataArray;
  }

  async addHumidityDataPoint() {
    const { city } = this.state;
    const arrayWithDataPoints = await this.getHumidityDataPoint(city);
    this.setState((prevState) => {
      return {
        chartData: {
          datasets: [
            {
              ...prevState.chartData.datasets[0],
              data: arrayWithDataPoints,
            },
          ],
        },
      };
    });
  }

  changeCity(newCity: string) {
    this.setState({ city: newCity });
  }

  render() {
    const { chartData } = this.state;

    const chartOptions = {
      scales: {
        x: {
          type: "time" as const,
          time: {
            unit: "second" as const,
            displayFormats: {
              second: "HH:mm:ss",
            },
          },
        },
      },
    };

    return (
      <div className="humidity">
        <div className="content">
          <div className="buttons">
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Berlin")}
              sx={{
                bgcolor:
                  this.state.city === "Berlin" ? "rgb(197, 14, 31)" : "white",
                color: this.state.city === "Berlin" ? "white" : "text.primary",
                ":hover": {
                  bgcolor: "rgb(197, 14, 31)",
                  color: "white",
                },
                borderColor: "text.primary",
              }}
            >
              Berlin
            </Button>
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Hamburg")}
              sx={{
                bgcolor:
                  this.state.city === "Hamburg" ? "rgb(197, 14, 31)" : "white",
                color: this.state.city === "Hamburg" ? "white" : "text.primary",
                ":hover": {
                  bgcolor: "rgb(197, 14, 31)",
                  color: "white",
                },
                borderColor: "text.primary",
              }}
            >
              Hamburg
            </Button>
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Munich")}
              sx={{
                bgcolor:
                  this.state.city === "Munich" ? "rgb(197, 14, 31)" : "white",
                color: this.state.city === "Munich" ? "white" : "text.primary",
                ":hover": {
                  bgcolor: "rgb(197, 14, 31)",
                  color: "white",
                },
                borderColor: "text.primary",
              }}
            >
              München
            </Button>
          </div>
          <div className="graphs">
            <Line data={chartData} options={chartOptions} id="chart1" />
          </div>
        </div>
      </div>
    );
  }
}

export default Humidity;
