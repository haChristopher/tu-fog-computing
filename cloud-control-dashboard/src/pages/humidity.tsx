import { Component } from "react";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import "./home.css";

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
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
          },
        ],
      },
    };

    this.addHumidityDataPoint = this.addHumidityDataPoint.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addHumidityDataPoint, 1000);
  }

  // hier GET data einbauen
  async getHumidityDataPoint() {
    // const berlin = "http://127.0.0.1:5000/api/v2/get_single?city=Berlin";
    const response = await fetch(
      "http://127.0.0.1:5000/api/v2/get_single?city=Berlin"
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
    const arrayWithDataPoints = await this.getHumidityDataPoint();
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
          {/* <p>Humidity</p> */}
          <div className="graphs">
            <Line data={chartData} options={chartOptions} id="chart1" />
          </div>
        </div>
      </div>
    );
  }
}

export default Humidity;
