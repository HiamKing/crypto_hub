import { useState, useEffect } from "react";
import PostFilters from "./filters";
import PostList from "./list";

export default function CoinMarketCapPosts() {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        
    }, []);


    return (
        <>
            <PostFilters />
            <PostList />
        </>
    );
}
