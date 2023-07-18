import { useState } from "react";
import CoinMarketCapNews from "../News";
import CoinMarketCapPosts from "../Posts";
import { TabNavItem, TabContent } from "components/utils/tab";

export default function CoinMarketCapTabBar() {
    const [activeTab, setActiveTab] = useState("posts");

    return (
        <div className="tab-bar">
            <ul className="nav">
                <TabNavItem
                    title="Posts"
                    id="posts"
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
                <TabNavItem
                    title="News"
                    id="news"
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
            </ul>

            <div className="outlet">
                <TabContent id="posts" activeTab={activeTab}>
                    <CoinMarketCapPosts />
                </TabContent>
                <TabContent id="news" activeTab={activeTab}>
                    <CoinMarketCapNews />
                </TabContent>
            </div>
        </div>
    );
}
