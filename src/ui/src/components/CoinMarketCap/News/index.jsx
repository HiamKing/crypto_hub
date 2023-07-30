import { useState, useEffect } from "react";
import NewsFilters from "./filters";
import { newsColsRenderers } from "./renderers";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import APIS from "services/apis";

function usePaginationModel({ filters, setFilters }) {
    const [paginationModel, setPaginationModel] = useState({
        pageSize: 25,
        page: 0,
    });

    const setPaginationAndFilters = (props) => {
        setPaginationModel(props);
        setFilters({
            ...filters,
            limit: props.pageSize,
            offset: props.page * props.pageSize,
        });
    };

    return [paginationModel, setPaginationAndFilters];
}

export default function CoinMarketCapNews() {
    const [isLoading, setIsLoading] = useState(false);
    const [news, setNews] = useState([]);
    const [rowCount, setRowCount] = useState(0);
    const [filters, setFilters] = useState({
        filters: {},
        limit: 25,
        offset: 0,
        with_count: true,
        sort_by: "updated_at",
    });
    const [paginationModel, setPaginationAndFilters] = usePaginationModel({
        filters,
        setFilters,
    });

    useEffect(() => {
        setIsLoading(true);
        APIS.cmc
            .search_news(filters)
            .then((res) => {
                const data = res.data;
                setNews(data["models"]);
                setRowCount(data["count"]);
                setIsLoading(false);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    }, [filters]);

    return (
        <>
            <NewsFilters filters={filters} setFilters={setFilters} />
            <Box sx={{ height: "100%", width: "73%" }}>
                <DataGrid
                    slots={{
                        columnHeaders: () => null,
                    }}
                    getRowHeight={() => "auto"}
                    getRowId={(row) => row._id}
                    columns={newsColsRenderers}
                    rows={news}
                    rowCount={rowCount}
                    loading={isLoading}
                    paginationModel={paginationModel}
                    paginationMode="server"
                    onPaginationModelChange={setPaginationAndFilters}
                    sx={{
                        "& .MuiDataGrid-virtualScroller::-webkit-scrollbar": {
                            display: "none",
                        },
                    }}
                />
            </Box>
        </>
    );
}
