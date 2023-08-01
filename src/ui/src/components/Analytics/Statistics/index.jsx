import { useState } from "react";
import Box from "@mui/material/Box";
import { symbolOptions } from "./constants";
import AnalyticsFilters from "../filters";

export default function Statistics() {
    const [symbol, setSymbol] = useState(0);
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [granularity, setGranularity] = useState("");

    return (
        <>
            <Box className="mt-1" sx={{ height: "100%", width: "25%" }}>
                <AnalyticsFilters
                    symbolOptions={symbolOptions}
                    setCurrentSymbol={setSymbol}
                    setStartTime={setStartTime}
                    setEndTime={setEndTime}
                    setGranularity={setGranularity}
                />
            </Box>
            <Box className="" sx={{ height: "100%", width: "75%" }}>
                {/* <RealTimeCandlestickChart symbol={currentSymbol} /> */}
            </Box>
        </>
    );
}
