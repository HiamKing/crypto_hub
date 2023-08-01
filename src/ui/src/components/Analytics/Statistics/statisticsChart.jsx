import ReactApexChart from "react-apexcharts";
import dayjs from "dayjs";

export default function StatisticsChart({ symbol, series, categories}) {
    const options = {
        chart: {
            type: "bar",
            stacked: true,
            toolbar: {
                show: true,
            },
            zoom: {
                enabled: true,
            },
        },
        xaxis: {
            type: "datetime",
            categories: categories,
            labels: {
                datetimeUTC: false,
            },
        },
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 10,
                dataLabels: {
                    total: {
                        enabled: true,
                        style: {
                            fontSize: "13px",
                            fontWeight: 900,
                        },
                    },
                },
            },
        },
        legend: {
            position: "top",
        },
        title: {
            text: `Statistics of CoinMarketCap posts and news for ${symbol}`,
            align: "center",
            style: {
                fontSize: "20px",
                fontWeight: "bold",
                color: "#333",
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

    return (
        <ReactApexChart
            options={options}
            series={series}
            type="bar"
            height={400}
        />
    );
}
