import { useState, useEffect } from "react";
import PostFilters from "./filters";
import { postColsRenderers } from "./renderers";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import APIS from "services/apis";

export default function CoinMarketCapPosts() {
    const [posts, setPosts] = useState([]);
    const [filters, setFilters] = useState({
        filters: {},
        limit: 30,
        offset: 0,
        with_count: true,
        sort_by: "post_time",
    });

    useEffect(() => {
        APIS.cmc
            .search_posts(filters)
            .then((res) => {
                const data = res.data;
                console.log(data)
                setPosts(data["models"]);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    }, []);

    return (
        <>
            <PostFilters />
            <Box sx={{ height: "100%", width: "75%" }}>
                <DataGrid
                    slots={{
                        columnHeaders: () => null,
                    }}
                    getRowHeight={() => 'auto'}
                    getRowId={(row) => row._id}
                    columns={postColsRenderers}
                    rows={posts}
                />
            </Box>
        </>
    );
}
