import {createBrowserRouter} from "react-router-dom";
import Preview from "../components/preview/Preview";
import {Home} from "../components/home/Home";
import React from "react";
import {Taxis} from "../components/taxi/Taxis";
import {Trips} from "../components/trip/Trips";
import {Order} from "../components/order/Order";
export const router = createBrowserRouter([
    {
        path: "/",
        element: <Home/>,
        children: [
            {
                index: true,
                element: <Preview/>
            },
            {
                path: "taxis",
                element: <Taxis/>
            },
            {
                path: "trips",
                element: <Trips/>
            },
            {
                path: "order",
                element: <Order/>
            }
        ],
    },
]);