import Header from "components/Header";
import { Outlet } from "react-router-dom";
import "./styles.scss";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import Dayjs from "dayjs";

Dayjs.extend(utc);
Dayjs.extend(relativeTime);

export default function App() {
    return (
        <>
            <div className="app">
                <Header />
                <div className="app-body">
                    <Outlet />
                </div>
            </div>
        </>
    );
}
