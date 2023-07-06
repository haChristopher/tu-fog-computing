import { Component } from "react";
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
    };

    this.addTempDataPoint = this.addTempDataPoint.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addTempDataPoint, 5000);
  }

  // hier GET data einbauen
  async getTempDataPoints() {
    // const berlin = "http://127.0.0.1:5000/api/v2/get_single?city=Berlin";
    const response = await fetch(
      "http://127.0.0.1:5000/api/v2/get_single?city=Berlin"
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
      // console.log(timeMeasurement, date, `Temperature: ${temp}`);

      // unshift will put it at the beginning of the array (order is then correct)
      temperatureDataArray.unshift(dataPoint);
    }
    return temperatureDataArray;
  }

  async addTempDataPoint() {
    const arrayWithDataPoints = await this.getTempDataPoints();
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
      <div className="temperature">
        <div className="content">
          {/* <p>Temperature</p> */}
          <div className="graphs">
            {/* "Line" creates line chart */}
            <Line data={chartData} options={chartOptions} id="chart1" />
          </div>
        </div>
      </div>
    );
  }
}

export default Temperature;
