import axios from 'axios';
import { useState, useEffect } from 'react';


import Calender from "../calender/Calender";
import DateDay from "../calender/DateDay";
import BookingData from '../bookingData/BookingData';


export default function () {
    const [date, setDate] = useState(new Date());
    const [bookingData, setBookingData] = useState({});
    const [isLoading, setIsLoading] = useState(false);


    const handleChange = async () => {
        setIsLoading(true);
        let uri = `https://sgtd.onrender.com/get-events/${date.getFullYear()}-${(date.getMonth() + 1) < 10 ? `0${ date.getMonth() + 1 }` : date.getMonth() + 1}-${date.getDate()}/1`;
        await axios({
            method: 'get',
            url: uri,
        }).then(async (res) => {
            setBookingData(res.data);
        });
        setIsLoading(false);
    }


    useEffect(() => {
        handleChange();
    }, [date]);


    return (
        <div className = 'pt-28 mx-5 my-10 flex flex-col justify-center align-center'>
            <Calender changeDate = { setDate } />
            <DateDay date = { date } />
            <BookingData isLoading = { isLoading } data = { bookingData } />
        </div>
    )
}