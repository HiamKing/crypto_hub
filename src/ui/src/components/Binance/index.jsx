import { useState } from "react";
import RealTimePriceTable from "./realtimePriceTable";
import RealTimeCandlestickChart from "./candlestickChart";
import Box from "@mui/material/Box";
import "./styles.scss";

export default function CoinMarketCap() {
    const [currentSymbol, setCurrentSymbol] = useState("BTCUSDT");

    return (
        <div className="d-flex">
            <Box className="mt-1" sx={{ height: "100%", width: "30%" }}>
                <RealTimePriceTable setCurrentSymbol={setCurrentSymbol} />
            </Box>
            <Box className="mt-1" sx={{ height: "100%", width: "70%" }}>
                <RealTimeCandlestickChart symbol={currentSymbol} />
            </Box>
        </div>
    );
}
