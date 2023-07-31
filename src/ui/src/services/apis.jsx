import axios from "axios";

const API_ROOT = process.env.REACT_APP_API_ROOT || "";

const APIS = {
    binance: {
        get_price_change: () => axios.get(`${API_ROOT}/binance/price-change`),
        get_symbol_klines: (symbol, interval) =>
            axios.get(`${API_ROOT}/binance/klines/${symbol}/${interval}`),
        get_symbol_24h_stats: (symbol) =>
        axios.get(`${API_ROOT}/binance/${symbol}/24h-stats`),
    },
    cmc: {
        search_posts: (args) =>
            axios.post(`${API_ROOT}/coin-market-cap/search-posts`, args),
        search_news: (args) =>
            axios.post(`${API_ROOT}/coin-market-cap/search-news`, args),
    },
};
// getOverviewInfo: (args) =>
// axios.get(`${API_ROOT}/get_overview`, { params: args }),
// runAlgorithm: (algorithm, args) =>
// axios.get(`${API_ROOT}/run_algorithm/${algorithm}`, { params: args }),
export default APIS;
