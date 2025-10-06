import React from "react";
import {NavLink, Outlet} from "react-router-dom";
import {AppBar, Button, Toolbar,} from "@mui/material";

export interface Props extends React.PropsWithChildren {

}

export const Home: React.FC = ({children}: Props) => (
    <>
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" component={NavLink} to="/"
                        end
                        sx={{
                            mr: 2,
                            textDecoration: (theme) => 'none', // default
                            '&.active': {
                                textDecoration: 'underline', // underline when active
                            },
                        }}>

                    Home
                </Button>
                <Button color="inherit" component={NavLink} to="/order" sx={{
                    mr: 2,
                    textDecoration: (theme) => 'none', // default
                    '&.active': {
                        textDecoration: 'underline', // underline when active
                    },
                }}>
                    Order
                </Button>
                <Button color="inherit" component={NavLink} to="/trips" sx={{
                    mr: 2,
                    textDecoration: (theme) => 'none', // default
                    '&.active': {
                        textDecoration: 'underline', // underline when active
                    },
                }}>
                    Trips
                </Button>
                <Button color="inherit" component={NavLink} to="/taxis" sx={{
                    mr: 2,
                    textDecoration: (theme) => 'none', // default
                    '&.active': {
                        textDecoration: 'underline', // underline when active
                    },
                }}>
                    Taxis
                </Button>
            </Toolbar>
        </AppBar>
        <Outlet/>
    </>
);