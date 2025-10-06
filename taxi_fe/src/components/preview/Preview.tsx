
import './Preview.css';
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, LabelList, ResponsiveContainer } from "recharts";
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
import {TaxiPos} from "../../models/dto";
import {fetchTaxiPos} from "../../api/taxis";

function Preview(): React.JSX.Element {
  const { data: taxiPositions = [], isLoading } = useQuery({
    queryKey: ["taxis"],
    queryFn: fetchTaxiPos,
    refetchInterval: 1000,
    placeholderData: []
  });

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold" align="center">
        Taxi-User Points on Grid
      </Typography>

      <Paper sx={{ height: 400, p: 2, mb: 4 }}>
        {isLoading ? (
          <div className="flex justify-center items-center h-full">
            <CircularProgress />
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid />
              <XAxis type="number" dataKey="x" name="X" />
              <YAxis type="number" dataKey="y" name="Y" />
              <Tooltip cursor={{ strokeDasharray: "3 3" }} />
              <Scatter name="Points" data={taxiPositions} fill="#1976d2">
                <LabelList dataKey={(p) => `${p.user_id}/${p.taxi_id}`} position="top" />
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        )}
      </Paper>

      <Typography variant="h6" gutterBottom>
        Point Data
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>User ID</TableCell>
              <TableCell>Taxi ID</TableCell>
              <TableCell>X</TableCell>
              <TableCell>Y</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {taxiPositions.map((p, i) => (
              <TableRow key={i}>
                <TableCell>{p.user_id}</TableCell>
                <TableCell>{p.taxi_id}</TableCell>
                <TableCell>{p.x}</TableCell>
                <TableCell>{p.y}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default Preview;
