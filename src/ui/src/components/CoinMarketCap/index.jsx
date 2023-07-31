import CoinMarketCapTabBar from "./TabBar";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import "./styles.scss";

export default function CoinMarketCap() {
    return (
        <>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <CoinMarketCapTabBar />
            </LocalizationProvider>
        </>
    );
}
