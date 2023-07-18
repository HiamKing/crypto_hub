function TabNavItem({ id, title, activeTab, setActiveTab }) {
    const handleClick = () => {
        setActiveTab(id);
    };

    return (
        <li onClick={handleClick} className={activeTab === id ? "active" : ""}>
            {title}
        </li>
    );
}

function TabContent({ id, activeTab, children }) {
    return activeTab === id ? (
        <div className="tab-content">{children}</div>
    ) : null;
};

export {TabNavItem, TabContent}
