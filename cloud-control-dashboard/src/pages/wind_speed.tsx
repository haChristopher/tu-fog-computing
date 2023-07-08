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

class WindSpeed extends Component<{}, State> {
  private interval: NodeJS.Timeout | null = null;

  constructor(props: any) {
    super(props);

    this.state = {
      chartData: {
        datasets: [
          {
            label: "Wind speed",
            data: [],
            fill: false,
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
          },
        ],
      },
      city: "Berlin", // Default city
    };

    this.addWindDataPoint = this.addWindDataPoint.bind(this);
    this.changeCity = this.changeCity.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addWindDataPoint, 1000);
  }

  // hier GET data einbauen
  async getWindDataPoint(city: string) {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v2/get_single?city=${city}`
    );
    const data = await response.json();
    let windDataArray = [];

    for (let i = 0; i < data.length; i++) {
      // unix timestamp
      let timeMesurement = data[i].time_of_measurement;
      // convert to date
      let date = new Date(timeMesurement * 1000).toISOString();

      let wind = data[i].wind_speed;
      let dataPoint = { x: date, y: wind };
      // console.log(timeMesurement, date, `Wind: ${wind}`);

      windDataArray.push(dataPoint);
    }
    return windDataArray;
  }

  async addWindDataPoint() {
    const { city } = this.state;
    const arrayWithDataPoints = await this.getWindDataPoint(city);
    // console.log("Inside the addRandomDataPoint", arrayWithDataPoint);
    // for (let i = 0; i < arrayWithDataPoints.length; i++) {
    //   let newDataPoint = arrayWithDataPoints[i];

    this.setState((prevState) => {
      //const newData = [...prevState.chartData.datasets[0].data];
      //newData.push(newDataPoint);

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
      <div className="wind-speed">
        <div className="content">
          <div className="buttons">
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Berlin")}
            >
              Berlin
            </Button>
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Hamburg")}
            >
              Hamburg
            </Button>
            <Button
              variant="outlined"
              onClick={() => this.changeCity("Munich")}
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

export default WindSpeed;
