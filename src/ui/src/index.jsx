import React from 'react';
import ReactDOM from 'react-dom/client';
import App from 'components/index';
import Home from 'components/Home/index';
import Binance from 'components/Binance/index';
import CoinMarketCap from 'components/CoinMarketCap/index';
import Analytics from 'components/Analytics';
import { routingPaths } from 'common/routers';
import {
    Route,
    createBrowserRouter,
    createRoutesFromElements,
    RouterProvider,
} from 'react-router-dom';
import './styles.scss';

const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path={routingPaths.home} element={<App />}>
            <Route path={routingPaths.home} element={<Home />} />
            <Route path={routingPaths.binance} element={<Binance />} />
            <Route path={routingPaths.coinMarketCap} element={<CoinMarketCap />} />
            <Route path={routingPaths.analytics} element={<Analytics />} />
            {/* <Route
                path={routingPaths.detailAlgorithm}
                element={<DetailAlgorithm />}
            /> */}
        </Route>
    )
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
