import RealTimePriceTable from "./realtimePriceTable";
import Box from "@mui/material/Box";
import "./styles.scss";

export default function CoinMarketCap() {
    return (
        <Box className="mt-1" sx={{ height: "100%", width: "30%" }}>
            <RealTimePriceTable />
        </Box>
    );
}
