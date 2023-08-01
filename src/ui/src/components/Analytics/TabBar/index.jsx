import { useState } from "react";
import Statistics from "../Statistics";
import Relations from "../Relations";
import { TabNavItem, TabContent } from "components/utils/tab";

export default function AnalyticsTabBar() {
    const [activeTab, setActiveTab] = useState("statistics");

    return (
        <div className="tab-bar">
            <ul className="nav">
                <TabNavItem
                    title="Statistics"
                    id="statistics"
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
                <TabNavItem
                    title="Relations"
                    id="relations"
                    activeTab={activeTab}
                    setActiveTab={setActiveTab}
                />
            </ul>

            <div className="outlet">
                <TabContent id="statistics" activeTab={activeTab}>
                    <Statistics />
                </TabContent>
                <TabContent id="relations" activeTab={activeTab}>
                    <Relations />
                </TabContent>
            </div>
        </div>
    );
}
