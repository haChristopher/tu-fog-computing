import { Component } from "react";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import "./home.css";
import { Button } from "@mui/material";

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

class Temperature extends Component<{}, State> {
  private interval: NodeJS.Timeout | null = null;
  constructor(props: any) {
    super(props);

    this.state = {
      chartData: {
        datasets: [
          {
            label: "Temperature",
            data: [],
            fill: false,
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
          },
        ],
      },
      city: "Berlin", // Default city
    };

    this.addTempDataPoint = this.addTempDataPoint.bind(this);
    this.changeCity = this.changeCity.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addTempDataPoint, 1000);
  }

  async getTempDataPoints(city: string) {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v2/get_single?city=${city}`
    );
    const data = await response.json();

    let temperatureDataArray = [];

    for (let i = 0; i < data.length; i++) {
      // unix timestamp
      let timeMeasurement = data[i].time_of_measurement;
      // convert to date
      let date = new Date(timeMeasurement * 1000).toISOString();

      let temp = data[i].temperature;
      let dataPoint = { x: date, y: temp };

      // unshift will put it at the beginning of the array (order is then correct)
      temperatureDataArray.unshift(dataPoint);
    }
    return temperatureDataArray;
  }

  async addTempDataPoint() {
    const { city } = this.state;
    const arrayWithDataPoints = await this.getTempDataPoints(city);
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

  public changeCity(newCity: string) {
    this.setState({ city: newCity });
  }

  render() {
    const { chartData, city } = this.state;

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
      <div className="temperature">
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

export default Temperature;
