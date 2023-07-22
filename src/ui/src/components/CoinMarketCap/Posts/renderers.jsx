import { useState } from "react";
import relativeTime from "dayjs/plugin/relativeTime";
import Dayjs from "dayjs";
import Chip from "@mui/material/Chip";
import AddReactionOutlinedIcon from "@mui/icons-material/AddReactionOutlined";
import TextsmsOutlinedIcon from "@mui/icons-material/TextsmsOutlined";
import Tooltip from "@mui/material/Tooltip";
import AutorenewOutlinedIcon from "@mui/icons-material/AutorenewOutlined";
import "./styles.scss";
import utc from "dayjs/plugin/utc";
Dayjs.extend(utc);
Dayjs.extend(relativeTime);

function TruncateText({ text }) {
    const [isReadMore, setIsReadMore] = useState(false);
    const MAX_LENGTH = 100;

    const toggleReadMore = () => {
        setIsReadMore(!isReadMore);
    };
    console.log(text.length)
    return (
        <div className="post-attribute content">
            {isReadMore
                ? text
                : text.substring(0, MAX_LENGTH)}
            {(text.length > MAX_LENGTH) &&
            (
                <span onClick={toggleReadMore} className="read-or-hide">
                    {!isReadMore ? "... Read more" : " Show less"}
                </span>
            )}
        </div>
    );
}

const postColsRenderers = [
    {
        field: "data",
        headerName: "Data",
        width: 861,
        renderCell: (row) => {
            return (
                <div>
                    <TruncateText text={row["row"]["text_content"]} />
                    <div className="post-attributes">
                        <div className="post-attribute">
                            {row["row"]["bullish"] !== null ? (
                                <Chip
                                    style={{
                                        backgroundColor: `${
                                            row["row"]["bullish"] == true
                                                ? "#16c784"
                                                : "#ea3943"
                                        }`,
                                        color: "#fff",
                                        fontSize: "0.7rem",
                                        fontWeight: "Bold",
                                        borderRadius: "8px",
                                        height: "1.4rem",
                                    }}
                                    label={`${
                                        row["row"]["bullish"] == true
                                            ? "▲ Bullish"
                                            : "▼ Bearish"
                                    }`}
                                />
                            ) : null}
                        </div>
                        <div className="post-attribute">
                            <AddReactionOutlinedIcon />
                            <span className="text-center ml-2">
                                {row["row"]["like_count"]}
                            </span>
                        </div>
                        <div className="post-attribute">
                            <TextsmsOutlinedIcon />
                            <span className="text-center ml-2">
                                {row["row"]["comment_count"]}
                            </span>
                        </div>
                        <div className="post-attribute">
                            <AutorenewOutlinedIcon />
                            <span className="text-center ml-2">
                                {row["row"]["repost_count"]}
                            </span>
                        </div>
                        <div className="post-attribute">
                            <Tooltip
                                title={Dayjs(row["row"]["post_time"])
                                    .utc(true)
                                    .toString()}
                                arrow
                            >
                                {Dayjs(row["row"]["post_time"])
                                    .utc(true)
                                    .fromNow()}
                            </Tooltip>
                        </div>
                    </div>
                </div>
            );
        },
    },
];

export { postColsRenderers };
