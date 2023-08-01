import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import ClearableDatePicker from "components/utils/clearableDateTimePicker";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import _ from "lodash"

export default function AnalyticsFilters({
    symbolOptions,
    setSymbol,
    setStartTime,
    setEndTime,
    setGranularity,
    fetchStatistics,
}) {
    const updateStartTime = (newStartTime) => {
        setStartTime(newStartTime.toISOString());
    };

    const updateEndtime = (newEndTime) => {
        setEndTime(newEndTime.toISOString());
    };

    const StartClearableDatePicker = (props) => {
        return <ClearableDatePicker props={props} setTime={updateStartTime} />;
    };

    const EndClearableDatePicker = (props) => {
        return <ClearableDatePicker props={props} setTime={updateEndtime} />;
    };

    return (
        <div className="filter-list">
            <div className="form-group">
                <label for="symbolInput">Symbol</label>
                <Autocomplete
                    disablePortal
                    size="small"
                    id="symbolInput"
                    options={symbolOptions}
                    onChange={(e, newVal) => setSymbol(_.get(newVal, "label", ""))}
                    renderInput={(params) => <TextField {...params} />}
                />
            </div>
            <div className="form-group">
                <label for="startTimeInput">Start Time</label>
                <DateTimePicker
                    views={["year", "day", "hours"]}
                    ampm={false}
                    slotProps={{ textField: { size: "small" } }}
                    onChange={updateStartTime}
                    slots={{ textField: StartClearableDatePicker }}
                />
            </div>
            <div className="form-group">
                <label for="endTimeInput">End Time</label>
                <DateTimePicker
                    views={["year", "day", "hours"]}
                    ampm={false}
                    slotProps={{ textField: { size: "small" } }}
                    onChange={updateEndtime}
                    slots={{ textField: EndClearableDatePicker }}
                />
            </div>
            <div className="form-group">
                <label for="granularitySelect">Granularity</label>
                <Autocomplete
                    disablePortal
                    size="small"
                    id="granularitySelect"
                    options={[
                        { label: "hour" },
                        { label: "day" },
                        { label: "month" },
                    ]}
                    onChange={(e, newVal) => setGranularity(_.get(newVal, "label", ""))}
                    renderInput={(params) => <TextField {...params} />}
                />
            </div>
            <div className="d-flex justify-content-center">
                <button type="button" class="btn btn-outline-dark" onClick={fetchStatistics}>
                    Search
                </button>
            </div>
        </div>
    );
}
