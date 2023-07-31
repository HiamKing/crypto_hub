import { routingPaths } from "common/routers";
import { NavLink } from "react-router-dom";
import logo from "./logo.png";
import "./styles.scss";

export default function Header() {
    return (
        <div className="header">
            <a className="header-link" href={routingPaths.home}>
                <img src={logo} alt="homepage" />
                <div className="logo-text">Crypto Hub</div>
            </a>
            <div className="header-btn">
                <NavLink className="header-btn-link" to={routingPaths.binance}>
                    Binance
                </NavLink>
            </div>
            <div className="header-btn">
                <NavLink
                    className="header-btn-link"
                    to={routingPaths.coinMarketCap}
                >
                    CoinMarketCap
                </NavLink>
            </div>
        </div>
    );
}
