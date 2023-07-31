import React, { useState, useEffect } from "react";
import ApexCharts from "react-apexcharts";
import dayjs from "dayjs";
import APIS from "services/apis";
import _ from "lodash";
import "./styles.scss";

const ButtonGroupComponent = ({ chartInterval, setChartInterval }) => {
    return (
        <div className="interval-group-btn">
            <span>Zoom</span>
            <span
                className={`interval-btn ${chartInterval === "1m" ? "active" : ""}`}
                onClick={() => setChartInterval("1m")}
            >
                1m
            </span>
            <span
                className={`interval-btn ${chartInterval === "1h" ? "active" : ""}`}
                onClick={() => setChartInterval("1h")}
            >
                1h
            </span>
            <span
                className={`interval-btn ${chartInterval === "1d" ? "active" : ""}`}
                onClick={() => setChartInterval("1d")}
            >
                1d
            </span>
            <span
                className={`interval-btn ${chartInterval === "1w" ? "active" : ""}`}
                onClick={() => setChartInterval("1w")}
            >
                1w
            </span>
            <span
                className={`interval-btn ${chartInterval === "1M" ? "active" : ""}`}
                onClick={() => setChartInterval("1M")}
            >
                1M
            </span>
        </div>
    );
};

const RealTimeCandlestickChart = ({ symbol }) => {
    const [chartInterval, setChartInterval] = useState("1m");
    const [candlestickData, setCandlestickData] = useState([]);
    const [volumeData, setVolumeData] = useState([]);

    const candlestickOptions = {
        chart: {
            type: "candlestick",
            height: 350,
        },
        xaxis: {
            type: "datetime",
            labels: {
                datetimeUTC: false,
                show: false,
            },
        },
        yaxis: {
            tooltip: {
                enabled: true,
            },
        },
        tooltip: {
            x: {
                formatter: function (val) {
                    return dayjs(val).format("YYYY-MM-DD HH:mm");
                },
            },
        },
    };

    const volumeOptions = {
        chart: {
            type: "bar",
            height: 160,
        },
        xaxis: {
            type: "datetime",
            labels: {
                datetimeUTC: false,
            },
        },
        plotOptions: {
            bar: {
                columnWidth: "80%",
            },
        },
        dataLabels: {
            enabled: false,
        },
        tooltip: {
            x: {
                formatter: function (val) {
                    return dayjs(val).format("YYYY-MM-DD HH:mm");
                },
            },
        },
    };

    const formatDataToChart = (data) => {
        const klinesData = [];
        const volumeData = [];
        for (const element of data) {
            const localTime = dayjs(element["start_time"])
                .utc(true)
                .local()
                .format("YYYY-MM-DDTHH:mm:ss");
            console.log(localTime);
            klinesData.push({
                x: localTime,
                y: [
                    element["open_price"],
                    element["high_price"],
                    element["low_price"],
                    element["close_price"],
                ],
            });
            volumeData.push({
                x: localTime,
                y: element["base_asset_vol"],
            });
        }
        setCandlestickData(klinesData);
        setVolumeData(volumeData);
    };

    const fetchRealTimeData = () => {
        if (!symbol || !chartInterval) {
            return
        }

        APIS.binance
            .get_symbol_klines(symbol, chartInterval)
            .then((res) => {
                const data = res.data;
                formatDataToChart(data["models"]);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    };

    useEffect(() => {
        fetchRealTimeData();

        const intervalId = setInterval(fetchRealTimeData, 2000); // Fetch data every 5 seconds

        // Clear interval on component unmount
        return () => clearInterval(intervalId);
    }, [symbol, chartInterval]);

    return (
        <div className="w-100">
            {symbol}
            <ButtonGroupComponent
                chartInterval={chartInterval}
                setChartInterval={setChartInterval}
            />
            {!_.isEmpty(candlestickData) && (
                <ApexCharts
                    options={candlestickOptions}
                    series={[{ data: candlestickData }]}
                    type="candlestick"
                    height={300}
                />
            )}
            {!_.isEmpty(volumeData) && (
                <ApexCharts
                    options={volumeOptions}
                    series={[{ name: "Volume", data: volumeData }]}
                    type="bar"
                    height={110}
                />
            )}
        </div>
    );
};

export default RealTimeCandlestickChart;
