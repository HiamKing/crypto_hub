import { useState, useEffect } from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
} from "@mui/material";
import SYMBOL_MAPPING from "common/symbolMapping";
import APIS from "services/apis";
import "./styles.scss";

function PairName({ symbol }) {
    const pairName = SYMBOL_MAPPING[symbol].split("/");
    const baseName = pairName[0];
    const quoteName = pairName[1];

    return (
        <div>
            <span className="base-name">{baseName}</span>
            <span>/</span>
            <span className="quote-name">{quoteName}</span>
        </div>
    );
}

function LastPrice({ lastPrice, priceChangePercent }) {
    return (
        <div>
            <span className={priceChangePercent > 0 ? "bullish" : "bearish"}>
                {lastPrice}
            </span>
        </div>
    );
}

function PriceChangePercent({ priceChangePercent }) {
    return (
        <div>
            <span className={priceChangePercent > 0 ? "bullish" : "bearish"}>
                {priceChangePercent}%
            </span>
        </div>
    );
}
export default function RealTimePriceTable(props) {
    const [tableData, setTableData] = useState([]);

    // Function to fetch real-time data from API
    const fetchRealTimeData = () => {
        // Replace this with your API endpoint to fetch the data
        // For example, you can use axios or fetch to make the API call
        // Here, I'm using a dummy data for demonstration purposes
        APIS.binance
            .get_price_change()
            .then((res) => {
                const data = res.data;
                setTableData(data["models"]);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    };

    // Fetch real-time data on component mount and set interval to fetch updates
    useEffect(() => {
        fetchRealTimeData();

        const intervalId = setInterval(fetchRealTimeData, 5000); // Fetch data every 5 seconds

        // Clear interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    return (
        <TableContainer component={Paper} className="realtime-price-table">
            <Table stickyHeader>
                <TableHead>
                    <TableRow>
                        <TableCell>Pair</TableCell>
                        <TableCell align="right">Price</TableCell>
                        <TableCell align="right">Change</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {tableData.map((row, index) => (
                        <TableRow
                            key={index}
                            className="realtime-price-table-row"
                            onClick={() => props.setCurrentSymbol(row.symbol)}
                        >
                            <TableCell component="th" scope="row">
                                <PairName symbol={row.symbol} />
                            </TableCell>
                            <TableCell align="right">
                                <LastPrice
                                    lastPrice={row.last_price}
                                    priceChangePercent={
                                        row.price_change_percent
                                    }
                                />
                            </TableCell>
                            <TableCell align="right">
                                <PriceChangePercent
                                    priceChangePercent={
                                        row.price_change_percent
                                    }
                                />
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
