import React, { useState, useEffect } from "react";
import ApexCharts from "react-apexcharts";
import dayjs from "dayjs";
import APIS from "services/apis";
import _ from "lodash";
import "./styles.scss";

const ButtonGroupComponent = ({ interval, setInterval }) => {
    return (
        <div className="interval-group-btn">
            <span>Zoom</span>
            <span
                className={`interval-btn ${interval === "1m" ? "active" : ""}`}
                onClick={() => setInterval("1m")}
            >
                1m
            </span>
            <span
                className={`interval-btn ${interval === "1h" ? "active" : ""}`}
                onClick={() => setInterval("1h")}
            >
                1h
            </span>
            <span
                className={`interval-btn ${interval === "1d" ? "active" : ""}`}
                onClick={() => setInterval("1d")}
            >
                1d
            </span>
            <span
                className={`interval-btn ${interval === "1w" ? "active" : ""}`}
                onClick={() => setInterval("1w")}
            >
                1w
            </span>
            <span
                className={`interval-btn ${interval === "1M" ? "active" : ""}`}
                onClick={() => setInterval("1M")}
            >
                1M
            </span>
        </div>
    );
};

const RealTimeCandlestickChart = ({ symbol }) => {
    const [interval, setInterval] = useState("1h");
    const [candlestickData, setCandlestickData] = useState([]);
    const [volumeData, setVolumeData] = useState([]);

    const candlestickOptions = {
        chart: {
            type: "candlestick",
            height: 350,
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            tooltip: {
                enabled: true,
            },
        },
        zoom: {
            enabled: true,
        },
    };

    const volumeOptions = {
        chart: {
            type: "bar",
            height: 160,
        },
        xaxis: {
            type: "datetime",
        },
        plotOptions: {
            bar: {
                columnWidth: "80%",
            },
        },
        dataLabels: {
            enabled: false,
        },
    };

    const formatDataToChart = (data) => {
        const klinesData = [];
        const volumeData = [];
        for (const element of data) {
            const localTime = dayjs(element["start_time"]).utc(true).local().format('YYYY-MM-DDTHH:mm:ss');
            console.log(localTime)
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
        APIS.binance
            .get_symbol_klines(symbol, interval)
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
    }, [symbol, interval]);

    return (
        <div className="w-100">
            {symbol}
            <ButtonGroupComponent
                interval={interval}
                setInterval={setInterval}
            />
            {!_.isEmpty(candlestickData) && (
                <ApexCharts
                    options={candlestickOptions}
                    series={[{ data: candlestickData }]}
                    type="candlestick"
                    he
                    ight={300}
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
