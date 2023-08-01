import { useState } from "react";
import Box from "@mui/material/Box";
import StatisticsChart from "./statisticsChart";
import { symbolOptions } from "./constants";
import APIS from "services/apis";
import AnalyticsFilters from "../filters";
import dayjs from "dayjs";
import _ from "lodash";

export default function Statistics() {
    const [symbol, setSymbol] = useState("");
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [granularity, setGranularity] = useState("");
    const [series, setSeries] = useState([]);
    const [categories, setCategories] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const fetchStatistics = () => {
        APIS.analytics
            .search_statistics({
                symbol: symbol,
                start_time: startTime,
                end_time: endTime,
                granularity: granularity,
            })
            .then((res) => {
                const data = res.data;
                const newSeries = [];
                console.log(data);
                newSeries.push({
                    name: "Posts count",
                    data: _.map(data["models"], (e) => e[1]),
                });
                newSeries.push({
                    name: "News count",
                    data: _.map(data["models"], (e) => e[2]),
                });
                setCategories(
                    _.map(data["models"], (e) =>
                        dayjs(e[0])
                            .utc(true)
                            .local()
                            .format("YYYY-MM-DDTHH:mm:ss")
                    )
                );
                setSeries(newSeries);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    };

    return (
        <>
            <Box className="mt-1" sx={{ height: "100%", width: "25%" }}>
                <AnalyticsFilters
                    symbolOptions={symbolOptions}
                    setSymbol={setSymbol}
                    setStartTime={setStartTime}
                    setEndTime={setEndTime}
                    setGranularity={setGranularity}
                    fetchStatistics={fetchStatistics}
                />
            </Box>
            <Box className="" sx={{ height: "100%", width: "75%" }}>
                <StatisticsChart symbol={symbol} series={series} categories={categories}/>
            </Box>
        </>
    );
}
