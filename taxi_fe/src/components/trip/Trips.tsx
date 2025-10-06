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
import {fetchTrips} from "../../api/taxis";

export function Trips() {
    const {data: trips = [], isLoading} = useQuery({
        queryKey: ["trips"],
        queryFn: fetchTrips,
        refetchInterval: 1000,
        placeholderData: []
    });

    return (
        <Container maxWidth="lg" sx={{py: 4}}>
            <Typography variant="h4" gutterBottom fontWeight="bold" align="center">
                Trips
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
                                    <TableCell>User ID</TableCell>
                                    <TableCell>Taxi ID</TableCell>
                                    <TableCell>Order ID</TableCell>
                                    <TableCell>Waiting Time</TableCell>
                                    <TableCell>Travel Time</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {trips.map((t, i) => (
                                    <TableRow key={i}>
                                        <TableCell>{t.user_id}</TableCell>
                                        <TableCell>{t.taxi_id}</TableCell>
                                        <TableCell>{t.order_id}</TableCell>
                                        <TableCell>{t.waiting_time}</TableCell>
                                        <TableCell>{t.travel_time}</TableCell>
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