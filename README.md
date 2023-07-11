# Fog Computing Project 🚀 | Summer Term 2023 TU Berlin
We are pleased to present our project, developed as part of the "Fog Computing" course at TU Berlin. In this endeavor, we focused on the development of an application for weather data collection using simulated sensors. Our main objective was to apply the concepts of Fog Computing to efficiently and reliably gather and process weather data.
For our simulation, we modeled three weather stations located in the cities of Hamburg, Berlin, and Munich. Each station continuously collects data on various meteorological parameters such as temperature, pressure, humidity, and wind speed. These data are of crucial importance for various applications, including weather forecasting, agriculture, and construction planning.
To efficiently capture and process the data, we opted for the Fog Computing approach. This involves leveraging a decentralized network of fog i.e. edge devices to perform data processing and storage closer to the data sources. This enables faster response to events, reduces data traffic to the central data center, and provides increased control over data privacy. Our application utilizes this Fog Computing architecture by capturing data from the simulated weather stations and transmitting it in real-time to the Fog devices. 
This README.md file will provide detailed insights into the architecture of our application, the implementation of the simulated sensors, and the algorithms employed for data processing. 

# Architecture

<p align="center">
<img src="documentation/figures/arch.drawio.png" alt="architecture" width="70%">
  <em>image_caption</em>
</p>

# Data generation

We used sensors to collect the weather data. We had two options for sourcing the data: (i) simulating the environmental data within a specific range or (ii) parsing live data from the weather API provided by www.weatherapi.com.

<p align="center">
<img src="documentation/figures/Sensors.png" alt="sensors" width="70%">
</p>

# Reliable messaging

As our solution operates in a distributed fog environment we need to consider that outages on multiple edge devices or server nodes could occur. To address this challenge we implemented several mechanisms to counteract such failures. This mechanisms ensure: (i) reading sensor data is never blocked by connection issues, (ii) failed data is persisted to disk and gets retried and (iii) if the Station fails after a restart the persisted data gets resend. For more information about the implemented mechanisms see the doc file.

<p align="center">
<img src="documentation/figures/reliable.drawio.png" alt="reliable messaging" width="70%">
</p>

The following picture shows a sample from the SQLite DB on one of the weather stations storing messages which were not able to be sent. Every entry has a unique id, a timestamp, a flag showing if it was sent or not, the number of sending attempts and then actual message body.

<p align="center">
<img src="documentation/figures/messages_db.png" alt="sensors" width="90%">
</p>


# Docker Compose for running Locally

All 3 components can be run locally using docker-compose
```
docker-compose up
```

After changes you need to rebuild
```
docker-compose build
```

Running a single service:

```
docker-compose up cloud-server
```
