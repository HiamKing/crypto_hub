import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import AnalyticsTabBar from "./TabBar";
import "./styles.scss"

export default function Analytics() {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <AnalyticsTabBar />
        </LocalizationProvider>
    );
}
