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

class Home extends Component<{}, State> {
  private interval: NodeJS.Timeout | null = null;

  constructor(props: any) {
    super(props);

    this.state = {
      chartData: {
        datasets: [
          {
            label: "Data",
            data: [],
            fill: false,
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
          },
        ],
      },
    };

    this.addRandomDataPoint = this.addRandomDataPoint.bind(this);
  }

  componentDidMount() {
    // Start the interval when the component mounts
    this.interval = setInterval(this.addRandomDataPoint, 3000);
  }

  componentWillUnmount() {
    // Clear the interval when the component unmounts
    if (this.interval) {
      clearInterval(this.interval);
    }
  }

  getRandomDataPoint(): DataPoint {
    const startTime = new Date().getTime();
    const time = new Date(startTime).toISOString();
    const value = Math.floor(Math.random() * 100);
    return { x: time, y: value };
  }

  addRandomDataPoint() {
    this.setState((prevState) => {
      const newData = [...prevState.chartData.datasets[0].data];
      const newDataPoint = this.getRandomDataPoint();
      newData.push(newDataPoint);

      return {
        chartData: {
          datasets: [
            {
              ...prevState.chartData.datasets[0],
              data: newData,
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
      <div className="main">
        <div className="header">
          <Typography variant="h5">Weather Station Dashboard</Typography>
        </div>

        <div className="content">
          <div className="buttons">
            <Button variant="outlined">Weather Station Berlin</Button>
            <Button variant="outlined">Weather Station Spain</Button>
            <Button variant="outlined">Weather Station USA</Button>
          </div>
          <div className="graphs">
            <Line data={chartData} options={chartOptions} id="chart1" />
          </div>
        </div>

        <div className="footer"></div>
      </div>
    );
  }
}

export default Home;
