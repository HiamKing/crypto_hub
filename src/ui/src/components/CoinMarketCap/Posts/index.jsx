import { useState, useEffect } from "react";
import PostFilters from "./filters";
import PostList from "./list";

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
                console.log(data);
            })
            .catch((e) => {
                console.log(`Error ${e}`);
            });
    }, []);

    return (
        <>
            <PostFilters />
            <PostList />
        </>
    );
}
