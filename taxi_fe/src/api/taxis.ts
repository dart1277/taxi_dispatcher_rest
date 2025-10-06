import {TaxiDetail, TaxiPos, Trip} from "../models/dto";

export const API_URL = process.env.REACT_APP_API_URL || "http://localhost:3000";
export const fetchTaxiPos = async (): Promise<TaxiPos[]> => {
    const res = await fetch(`${API_URL}/trip/positions`);
    const resJson = await res.json();
    if (!res.ok) {
        throw new Error(resJson.message);
    }
    return resJson;
};

export const fetchTrips = async (): Promise<Trip[]> => {
    const res = await fetch(`${API_URL}/trip`);
    return res.json();
};

export const fetchTaxis = async (): Promise<TaxiDetail[]> => {
    const res = await fetch(`${API_URL}/taxi`);
    return res.json();
};