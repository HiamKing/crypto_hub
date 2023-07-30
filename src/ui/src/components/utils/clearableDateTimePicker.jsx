import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import ClearIcon from "@mui/icons-material/Clear";

export default function ClearableDatePicker({ props, setTime }) {
    return (
        <>
            <TextField
                {...props}
                InputProps={{
                    endAdornment: (
                        <>
                            {props.value && (
                                <IconButton
                                    edge="end"
                                    onClick={() => setTime(null)}
                                >
                                    <ClearIcon />
                                </IconButton>
                            )}
                            {props.InputProps.endAdornment}
                        </>
                    ),
                }}
            />
        </>
    );
}
