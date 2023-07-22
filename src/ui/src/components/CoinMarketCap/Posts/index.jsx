import { useState, useEffect } from "react";
import PostFilters from "./filters";
import { postColsRenderers } from "./renderers";
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

export default function CoinMarketCapPosts() {
    const [isLoading, setIsLoading] = useState(false);
    const [posts, setPosts] = useState([]);
    const [rowCount, setRowCount] = useState(0);
    const [filters, setFilters] = useState({
        filters: {},
        limit: 25,
        offset: 0,
        with_count: true,
        sort_by: "post_time",
    });
    const [paginationModel, setPaginationAndFilters] = usePaginationModel({
        filters,
        setFilters,
    });

    useEffect(() => {
        console.log(filters);
        setIsLoading(true);
        APIS.cmc
            .search_posts(filters)
            .then((res) => {
                const data = res.data;
                setPosts(data["models"]);
                setRowCount(data["count"]);
                setIsLoading(false);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    }, [filters]);

    return (
        <>
            <PostFilters />
            <Box sx={{ height: "100%", width: "75%" }}>
                <DataGrid
                    slots={{
                        columnHeaders: () => null,
                    }}
                    getRowHeight={() => "auto"}
                    getRowId={(row) => row._id}
                    columns={postColsRenderers}
                    rows={posts}
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
