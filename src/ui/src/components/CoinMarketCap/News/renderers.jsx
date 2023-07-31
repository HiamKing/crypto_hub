import Dayjs from "dayjs";
import Tooltip from "@mui/material/Tooltip";
import "./styles.scss";

function Newscontent({ row }) {
    const MAX_LENGTH = 100;

    return (
        <div className="news-attribute content w-75">
            <div className="title">
                {row["title"].length <= MAX_LENGTH
                    ? row["title"]
                    : row["title"].substring(0, MAX_LENGTH) + "..."}
            </div>
            <div className="subtitle">
                {row["subtitle"].length <= MAX_LENGTH
                    ? row["subtitle"]
                    : row["subtitle"].substring(0, MAX_LENGTH) + "..."}
            </div>
            <div className="source-name">{row["source_name"]}</div>
        </div>
    );
}

const newsColsRenderers = [
    {
        field: "data",
        headerName: "Data",
        width: 838,
        renderCell: (row) => {
            return (
                <div className="w-100">
                    <div className="news-attribute">
                        <Tooltip
                            title={Dayjs(row["row"]["updated_at"])
                                .utc(true)
                                .local()
                                .format("ddd, DD MMM YYYY HH:mm:ss")}
                            arrow
                        >
                            {Dayjs(row["row"]["updated_at"])
                                .utc(true)
                                .fromNow()}
                        </Tooltip>
                    </div>
                    <a
                        className="news-attributes link"
                        href={row["row"]["source_url"]}
                        target="_blank"
                        rel="noreferrer"
                    >
                        <Newscontent row={row["row"]} />
                        <img
                            className="news-attribute cover"
                            src={row["row"]["cover"]}
                            alt=""
                        />
                    </a>
                </div>
            );
        },
    },
];

export { newsColsRenderers };
