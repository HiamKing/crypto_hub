import { useState } from "react";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import ClearableDatePicker from "components/utils/clearableDateTimePicker";
import _ from "lodash";

export default function PostFilters({ filters, setFilters }) {
    const [endTime, setEndTime] = useState(null);
    const [startTime, setStartTime] = useState(null);

    const updateKeyword = (event) => {
        const newFilters = {
            ...filters["filters"],
            text_content: event.target.value,
        };

        if (newFilters["text_content"] === "") {
            delete newFilters["text_content"];
        }

        setFilters({
            ...filters,
            filters: newFilters,
        });
    };

    const updateStartTime = (newStartTime) => {
        setStartTime(newStartTime);
        const newFilters = {...filters["filters"]};

        if (newStartTime === null) {
            if ("post_time" in newFilters && "$gte" in newFilters["post_time"]) {
                delete newFilters["post_time"]["$gte"]
            }
        } else {
            if (!("post_time" in newFilters)) {
                newFilters["post_time"] = {}
            }
            newFilters["post_time"]["$gte"] = newStartTime.toISOString()
        }

        if ("post_time" in newFilters && _.isEmpty(newFilters["post_time"])) {
            delete newFilters["post_time"]
        }

        setFilters({
            ...filters,
            filters: newFilters,
        });
    };

    const updateEndtime = (newEndTime) => {
        setEndTime(newEndTime);
        const newFilters = {...filters["filters"]};

        if (newEndTime === null) {
            if ("post_time" in newFilters && "$lte" in newFilters["post_time"]) {
                delete newFilters["post_time"]["$lte"]
            }
        } else {
            if (!("post_time" in newFilters)) {
                newFilters["post_time"] = {}
            }
            newFilters["post_time"]["$lte"] = newEndTime.toISOString()
        }
        if ("post_time" in newFilters && _.isEmpty(newFilters["post_time"])) {
            delete newFilters["post_time"]
        }

        setFilters({
            ...filters,
            filters: newFilters,
        });
    };

    const StartClearableDatePicker = (props) => {
        return <ClearableDatePicker props={props} setTime={updateStartTime} />
    }

    const EndClearableDatePicker = (props) => {
        return <ClearableDatePicker props={props} setTime={updateEndtime} />
    }

    return (
        <>
            <div className="filter-list">
                <div className="form-group">
                    <label for="keywordInput">Keyword</label>
                    <input
                        type="text"
                        className="form-control"
                        id="keywordInput"
                        placeholder="Enter keyword"
                        onChange={updateKeyword}
                    />
                </div>
                <div className="form-group">
                    <label for="startTimeInput">Start Time</label>
                    <DateTimePicker
                        views={["year", "day", "hours", "minutes", "seconds"]}
                        ampm={false}
                        value={startTime}
                        slotProps={{ textField: { size: "small" } }}
                        onChange={updateStartTime}
                        slots={{ textField: StartClearableDatePicker }}
                    />
                </div>
                <div className="form-group">
                    <label for="endTimeInput">End Time</label>
                    <DateTimePicker
                        views={["year", "day", "hours", "minutes", "seconds"]}
                        ampm={false}
                        value={endTime}
                        slotProps={{ textField: { size: "small" } }}
                        onChange={updateEndtime}
                        slots={{ textField: EndClearableDatePicker }}
                    />
                </div>
            </div>
        </>
    );
}
