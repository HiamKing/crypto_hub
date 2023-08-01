import { useState } from "react";
import Box from "@mui/material/Box";
import RelationsChart from "./relationsChart";
import { symbolOptions } from "./constants";
import APIS from "services/apis";
import AnalyticsFilters from "../filters";
import dayjs from "dayjs";
import _ from "lodash";

export default function Statistics() {
    const [symbol, setSymbol] = useState("");
    const [startTime, setStartTime] = useState(null);
    const [endTime, setEndTime] = useState(null);
    const [granularity, setGranularity] = useState("");
    const [baseSeries, setBaseSeries] = useState([]);
    const [quoteSeries, setQuoteSeries] = useState([]);
    const [baseCategories, setBaseCategories] = useState([]);
    const [quoteCategories, setQuoteCategories] = useState([]);

    const handleSeries = (data, setSeries, setCategories) => {
        const newSeries = [];
        newSeries.push({
            name: "Posts Count",
            type: "column",
            data: _.map(data, (e) => e[2]),
        });
        newSeries.push({
            name: "News Count",
            type: "column",
            data: _.map(data, (e) => e[3]),
        });
        newSeries.push({
            name: "Price",
            type: "line",
            data: _.map(data, (e) => e[1]),
        });
        setSeries(newSeries);
        setCategories(
            _.map(data, (e) =>
                dayjs(e[0]).utc(true).local().format("YYYY-MM-DDTHH:mm:ss")
            )
        );
    };

    const fetchStatistics = () => {
        console.log(symbol, startTime, endTime, granularity)
        if (symbol === "" || startTime === null || endTime === null || granularity === "") {
            return;
        }

        APIS.analytics
            .search_relations({
                symbol: symbol,
                start_time: startTime.toISOString(),
                end_time: endTime.toISOString(),
                granularity: granularity,
            })
            .then((res) => {
                const data = res.data;
                handleSeries(
                    data["base_series"],
                    setBaseSeries,
                    setBaseCategories
                );
                handleSeries(
                    data["quote_series"],
                    setQuoteSeries,
                    setQuoteCategories
                );
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
                    startTime={startTime}
                    setStartTime={setStartTime}
                    endTime={endTime}
                    setEndTime={setEndTime}
                    setGranularity={setGranularity}
                    fetchStatistics={fetchStatistics}
                />
            </Box>
            <Box className="" sx={{ height: "100%", width: "75%" }}>
                <RelationsChart
                    symbol={symbol}
                    baseSeries={baseSeries}
                    quoteSeries={quoteSeries}
                    baseCategories={baseCategories}
                    quoteCategories={quoteCategories}
                />
            </Box>
        </>
    );
}
