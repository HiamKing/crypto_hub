import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";

export default function PostFilters({ filters, setFilters }) {
    const updateKeyword = (event) => {
        const newFilters = {
            ...filters["filters"],
            text_content: event.target.value,
        };

        if (newFilters["text_content"] === "") {
            delete newFilters["text_content"]
        }

        setFilters({
            ...filters,
            filters: newFilters,
        });
    };

    return (
        <>
            <div className="filter-list">
                <form>
                    <div class="form-group">
                        <label for="keywordInput">Keyword</label>
                        <input
                            type="text"
                            class="form-control"
                            id="keywordInput"
                            placeholder="Enter keyword"
                            onChange={updateKeyword}
                        />
                    </div>
                    <div class="form-group">
                        <label for="startTimeInput">Start Time</label>
                        <DateTimePicker />
                    </div>
                    <div class="form-group">
                        <label for="endTimeInput">End Time</label>
                        <DateTimePicker />
                    </div>
                    <button type="submit" class="btn btn-outline-dark">
                        Search
                    </button>
                </form>
            </div>
        </>
    );
}
