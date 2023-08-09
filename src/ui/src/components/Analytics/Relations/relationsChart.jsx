import ReactApexChart from "react-apexcharts";
import dayjs from "dayjs";

export default function RelationsChart(props) {
    const { symbol, baseSeries, quoteSeries, baseCategories, quoteCategories } =
        props;

    if (baseSeries.length === 0) {
        return <></>
    }

    const priceMax =
        Math.max(...baseSeries[2]["data"]) + Math.max(...baseSeries[2]["data"]) / 100;
    const priceMin =
        Math.min(...baseSeries[2]["data"]) - Math.min(...baseSeries[2]["data"]) / 100;

    const getOptions = (symbol, categories) => {
        return {
            chart: {
                height: 350,
                type: "line",
                stacked: false,
            },
            dataLabels: {
                enabled: false,
            },
            title: {
                text: `CoinMarketCap news, posts and ${symbol} price`,
                align: "center",
                style: {
                    fontSize: "20px",
                    fontWeight: "bold",
                    color: "#333",
                },
            },
            xaxis: {
                type: "datetime",
                categories: categories,
                labels: {
                    datetimeUTC: false,
                },
            },
            yaxis: [
                {
                    axisTicks: {
                        show: true,
                    },
                    axisBorder: {
                        show: true,
                        color: "#008FFB",
                    },
                    labels: {
                        style: {
                            colors: "#008FFB",
                        },
                    },
                    title: {
                        text: "Number of Posts",
                        style: {
                            color: "#008FFB",
                        },
                    },
                    tooltip: {
                        enabled: true,
                    },
                },
                {
                    seriesName: "News Count",
                    opposite: true,
                    axisTicks: {
                        show: true,
                    },
                    axisBorder: {
                        show: true,
                        color: "#00E396",
                    },
                    labels: {
                        style: {
                            colors: "#00E396",
                        },
                    },
                    title: {
                        text: "Number of News",
                        style: {
                            color: "#00E396",
                        },
                    },
                },
                {
                    seriesName: "Price",
                    opposite: true,
                    axisTicks: {
                        show: true,
                    },
                    axisBorder: {
                        show: true,
                        color: "#FEB019",
                    },
                    labels: {
                        style: {
                            colors: "#FEB019",
                        },
                    },
                    title: {
                        text: `${symbol} price`,
                        style: {
                            color: "#FEB019",
                        },
                    },
                    max: priceMax,
                    min: priceMin,
                },
            ],
            tooltip: {
                x: {
                    formatter: function (val) {
                        return dayjs(val).format("YYYY-MM-DD HH:mm");
                    },
                },
            },
            legend: {
                position: "top",
            },
        };
    };

    return (
        <>
            <ReactApexChart
                options={getOptions(symbol.split("/")[0], baseCategories)}
                series={baseSeries}
                type="line"
                height={400}
            />
            <ReactApexChart
                options={getOptions(symbol.split("/")[1], quoteCategories)}
                series={quoteSeries}
                type="line"
                height={400}
            />
        </>
    );
}
