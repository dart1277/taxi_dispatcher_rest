import React, {useState} from "react";
import {Alert, Box, Button, Container, Paper, TextField, Typography,} from "@mui/material";
import {API_URL} from "../../api/taxis";


interface OrderForm {
    user_id: string;
    src_x: number | string;
    src_y: number | string;
    dst_x: number | string;
    dst_y: number | string;
}

function tryParse(val: any) {
    const num = parseInt(val);
    return Number.isNaN(num) ? val : num;
}

const initialState = {
    user_id: "",
    src_x: "",
    src_y: "",
    dst_x: "",
    dst_y: ""
};

export function Order() {
    const [form, setForm] = useState<OrderForm>(initialState);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");
    const [open, setOpen] = useState(false);

    const handleClose = (
        event?: React.SyntheticEvent | Event,
        reason?: string
    ) => {
        if (reason === 'clickaway') return; // prevent closing when clicking outside
        setOpen(false);
        setError("");
    };
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({...form, [e.target.name]: tryParse(e.target.value)});
    };

    const handleSubmit = async (e: React.FormEvent<HTMLInputElement>) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            const res = await fetch(`${API_URL}/order`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(form),
            });

            const resJson = await res.json();
            if (!res.ok) {
                throw new Error(resJson.message || "Error occurred");
            }

        } catch (e: any) {
            setError(e?.message || "An error occurred.");
            setOpen(true);
            setSubmitting(false);
            return;
        }
        setSubmitting(false);
        setForm(initialState);
        alert("Order submitted!");
    };

    return (
        <Container maxWidth="sm" sx={{py: 4}}>
            <Typography variant="h4" gutterBottom fontWeight="bold" align="center">
                Create Order
            </Typography>
            {open && <Alert onClose={handleClose} severity="error" variant="filled" style={{margin: '1rem'}}>
                {error}
            </Alert>}
            <Paper sx={{p: 3}}>
                <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
                    <TextField label="User email" name="user_id" type="email" value={form.user_id}
                               onChange={handleChange} required/>
                    <TextField label="X Start"
                               name="src_x"
                               type="number"
                               InputProps={{
                                   inputProps: {min: 1, max: 100, step: 1},
                               }}
                               helperText="Value must be between 1 and 100"
                               value={form.src_x}
                               onChange={handleChange} required/>
                    <TextField label="Y Start" name="src_y"
                               type="number"
                               InputProps={{
                                   inputProps: {min: 1, max: 100, step: 1},
                               }}
                               helperText="Value must be between 1 and 100"
                               value={form.src_y} onChange={handleChange} required/>
                    <TextField label="X End" name="dst_x"
                               type="number"
                               InputProps={{
                                   inputProps: {min: 1, max: 100, step: 1},
                               }}
                               helperText="Value must be between 1 and 100"
                               value={form.dst_x} onChange={handleChange} required/>
                    <TextField label="Y End" name="dst_y"
                               type="number"
                               InputProps={{
                                   inputProps: {min: 1, max: 100, step: 1},
                               }}
                               helperText="Value must be between 1 and 100"
                               value={form.dst_y} onChange={handleChange} required/>
                    <Button type="submit" variant="contained" disabled={submitting}>
                        {submitting ? "Submitting..." : "Submit Order"}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
}