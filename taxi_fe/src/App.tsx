import './App.css';
import React from "react";
import {RouterProvider} from "react-router-dom";
import {router} from "./routes/routes";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {ReactQueryDevtools} from "@tanstack/react-query-devtools";

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 2,
            staleTime: 5000, // 5 seconds
            refetchOnMount: true,
            refetchOnWindowFocus: true,
            refetchOnReconnect: true,
            refetchInterval: 5000, //5 seconds
            refetchIntervalInBackground: false,
        },
        mutations: {
            retry: 2,
        },
    },
});

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <RouterProvider router={router}/>
            <ReactQueryDevtools initialIsOpen={false}/>
        </QueryClientProvider>
    );
}

export default App;
