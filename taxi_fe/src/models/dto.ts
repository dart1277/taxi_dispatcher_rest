export interface TaxiPos {
    x: number;
    y: number;
    taxi_id: string
    user_id?: string
}

export interface TaxiDetail {
    cur_x: number;
    cur_y: number;
    src_x: number;
    src_y: number;
    dst_x: number;
    dst_y: number;
    taxi_id: string
    status: string
}

export interface Trip {
    user_id: string;
    taxi_id: string;
    order_id: string;
    waiting_time: string;
    travel_time: string;
    assignment_time: string;
}
