import { useState } from "react";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import ClearableDatePicker from "components/utils/clearableDateTimePicker";
import _ from "lodash";

export default function NewsFilters({ filters, setFilters }) {
    const [endTime, setEndTime] = useState(null);
    const [startTime, setStartTime] = useState(null);

    const updateKeyword = (event) => {
        const newFilters = {
            ...filters["filters"],
            title: event.target.value,
        };

        if (newFilters["title"] === "") {
            delete newFilters["title"];
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
            if ("updated_at" in newFilters && "$gte" in newFilters["updated_at"]) {
                delete newFilters["updated_at"]["$gte"]
            }
        } else {
            if (!("updated_at" in newFilters)) {
                newFilters["updated_at"] = {}
            }
            newFilters["updated_at"]["$gte"] = newStartTime.toISOString()
        }

        if ("updated_at" in newFilters && _.isEmpty(newFilters["updated_at"])) {
            delete newFilters["updated_at"]
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
            if ("updated_at" in newFilters && "$lte" in newFilters["updated_at"]) {
                delete newFilters["updated_at"]["$lte"]
            }
        } else {
            if (!("updated_at" in newFilters)) {
                newFilters["updated_at"] = {}
            }
            newFilters["updated_at"]["$lte"] = newEndTime.toISOString()
        }
        if ("updated_at" in newFilters && _.isEmpty(newFilters["updated_at"])) {
            delete newFilters["updated_at"]
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
