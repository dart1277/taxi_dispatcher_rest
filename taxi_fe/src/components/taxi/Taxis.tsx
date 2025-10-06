import React, {useState} from "react";
import {BrowserRouter as Router, Routes, Route, NavLink} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, LabelList, ResponsiveContainer} from "recharts";
import {
    Container,
    Typography,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    CircularProgress,
    AppBar,
    Toolbar,
    Button,
    TextField,
    Box,
} from "@mui/material";
import {fetchTaxis} from "../../api/taxis";

export function Taxis() {
    const {data: taxis = [], isLoading} = useQuery({
        queryKey: ["taxis"],
        queryFn: fetchTaxis,
        refetchInterval: 1000,
        placeholderData: []
    });

    return (
        <Container maxWidth="lg" sx={{py: 4}}>
            <Typography variant="h4" gutterBottom fontWeight="bold" align="center">
                Taxis
            </Typography>
            <Paper>
                {isLoading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" p={4}>
                        <CircularProgress/>
                    </Box>
                ) : (
                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Taxi ID</TableCell>
                                    <TableCell>Status</TableCell>
                                    <TableCell>X Position</TableCell>
                                    <TableCell>Y Position</TableCell>
                                    <TableCell>X Source</TableCell>
                                    <TableCell>Y Source</TableCell>
                                    <TableCell>X Destination</TableCell>
                                    <TableCell>Y Destination</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {taxis.map((t, i) => (
                                    <TableRow key={i}>
                                        <TableCell>{t.taxi_id}</TableCell>
                                        <TableCell>{t.status}</TableCell>
                                        <TableCell>{t.cur_x}</TableCell>
                                        <TableCell>{t.cur_y}</TableCell>
                                        <TableCell>{t.src_x ?? "-"}</TableCell>
                                        <TableCell>{t.src_y ?? "-"}</TableCell>
                                        <TableCell>{t.dst_x ?? "-"}</TableCell>
                                        <TableCell>{t.dst_y ?? "-"}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                )}
            </Paper>
        </Container>
    );
}