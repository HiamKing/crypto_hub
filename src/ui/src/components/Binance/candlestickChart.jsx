import React, { useState, useEffect } from "react";
import ApexCharts from "react-apexcharts";
import dayjs from "dayjs";
import APIS from "services/apis";
import _ from "lodash";
import SYMBOL_MAPPING from "common/symbolMapping";
import "./styles.scss";

function ButtonGroupComponent({ chartInterval, setChartInterval }) {
    return (
        <div className="interval-group-btn">
            <span>Zoom</span>
            <span
                className={`interval-btn ${
                    chartInterval === "1m" ? "active" : ""
                }`}
                onClick={() => setChartInterval("1m")}
            >
                1m
            </span>
            <span
                className={`interval-btn ${
                    chartInterval === "1h" ? "active" : ""
                }`}
                onClick={() => setChartInterval("1h")}
            >
                1h
            </span>
            <span
                className={`interval-btn ${
                    chartInterval === "1d" ? "active" : ""
                }`}
                onClick={() => setChartInterval("1d")}
            >
                1d
            </span>
            <span
                className={`interval-btn ${
                    chartInterval === "1w" ? "active" : ""
                }`}
                onClick={() => setChartInterval("1w")}
            >
                1w
            </span>
            <span
                className={`interval-btn ${
                    chartInterval === "1M" ? "active" : ""
                }`}
                onClick={() => setChartInterval("1M")}
            >
                1M
            </span>
        </div>
    );
}

function Symbol24Stats({ symbol }) {
    const [stats, setStats] = useState({});
    const pairName = SYMBOL_MAPPING[symbol];
    const baseName = pairName.split("/")[0];
    const quoteName = pairName.split("/")[1];

    const fetchRealTimeData = () => {
        if (!symbol) {
            return;
        }

        APIS.binance
            .get_symbol_24h_stats(symbol)
            .then((res) => {
                const data = res.data;
                setStats(data);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    };

    useEffect(() => {
        fetchRealTimeData();

        const intervalId = setInterval(fetchRealTimeData, 2000);

        // Clear interval on component unmount
        return () => clearInterval(intervalId);
    }, [symbol]);

    if (_.isEmpty(stats)) {
        return <></>;
    }

    return (
        <div className="d-flex">
            <div className="symbol-name h-100">{pairName}</div>
            <div className={"symbol-price " + stats["last_price_state"]}>
                <span>
                    {stats["last_price"].toLocaleString("en-US", {
                        maximumFractionDigits: 20,
                        minimumFractionDigits: 2,
                    })}
                </span>
            </div>
            <div className="symbol-stats-group">
                <div className="symbol-stats price">
                    <div className="label">24h Change</div>
                    <div
                        className={`value + ${
                            stats["price_change"] > 0 ? "bullish" : "bearish"
                        }`}
                    >{`${stats["price_change"]} ${stats["price_change_percent"]}%`}</div>
                </div>
                <div className="symbol-stats price">
                    <div className="label">24h High</div>
                    <div className="value">
                        {stats["high_price"].toLocaleString("en-US", {
                            maximumFractionDigits: 20,
                            minimumFractionDigits: 2,
                        })}
                    </div>
                </div>
                <div className="symbol-stats price">
                    <div className="label">24h Low</div>
                    <div className="value">
                        {stats["low_price"].toLocaleString("en-US", {
                            maximumFractionDigits: 20,
                            minimumFractionDigits: 2,
                        })}
                    </div>
                </div>
                <div className="symbol-stats volume">
                    <div className="label">24h Volume({baseName})</div>
                    <div className="value">
                        {stats["base_asset_vol"].toLocaleString("en-US", {
                            maximumFractionDigits: 2,
                            minimumFractionDigits: 2,
                        })}
                    </div>
                </div>
                <div className="symbol-stats volume">
                    <div className="label">24h Volume({quoteName})</div>
                    <div className="value">
                        {stats["quote_asset_vol"].toLocaleString("en-US", {
                            maximumFractionDigits: 2,
                            minimumFractionDigits: 2,
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}

function RealTimeCandlestickChart({ symbol }) {
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
            return;
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
            <Symbol24Stats symbol={symbol} />
            <ButtonGroupComponent
                chartInterval={chartInterval}
                setChartInterval={setChartInterval}
            />
            {!_.isEmpty(candlestickData) && (
                <ApexCharts
                    options={candlestickOptions}
                    series={[{ data: candlestickData }]}
                    type="candlestick"
                    height={265}
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
}

export default RealTimeCandlestickChart;
