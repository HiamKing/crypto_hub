import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';

const RealTimeCandlestickChart = () => {
  const [data, setData] = useState([]);
  const [volumeData, setVolumeData] = useState([]);
  const [options, setOptions] = useState({
    chart: {
      type: 'candlestick',
      height: 350,
    },
    xaxis: {
      type: 'category',
      labels: {
        formatter: (val) => new Date(val).toLocaleTimeString(),
      },
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  });

//   useEffect(() => {
//     const socket = io('wss://your-websocket-url'); // Replace with your actual WebSocket URL

//     socket.on('connect', () => {
//       console.log('Connected to WebSocket server');
//     });

//     socket.on('data', (newData) => {
//       setData((prevData) => [...prevData, { x: new Date().getTime(), ...newData }]);
//       setVolumeData((prevData) => [...prevData, { x: new Date().getTime(), y: newData.volume }]);
//     });

//     socket.on('disconnect', () => {
//       console.log('Disconnected from WebSocket server');
//     });

//     return () => {
//       socket.disconnect();
//     };
//   }, []);

  return (
    <div>
      {/* <ApexCharts options={options} series={[{ data }]} type="candlestick" height={350} />
      <ApexCharts options={options} series={[{ data: volumeData }]} type="bar" height={160} /> */}
    </div>
  );
};

export default RealTimeCandlestickChart;