import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';


import Calender from "../calender/Calender";
import DateDay from "../calender/DateDay";
import BookingData from '../bookingData/BookingData';


export default function () {
    const [date, setDate] = useState(new Date());
    const [bookingData, setBookingData] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const position = useSelector((state) => state.position);
    const navigate = useNavigate();


    const handleChange = async () => {
        setIsLoading(true);

        let uri = `https://sgtd.onrender.com/get-events/${date.getFullYear()}-${(date.getMonth() + 1) < 10 ? `0${ date.getMonth() + 1 }` : date.getMonth() + 1}-${date.getDate()}/1`;
        await axios({
            method: 'get',
            url: uri,
            headers : {
                'Access-Control-Allow-Origin': '*',
            }
        }).then(async (res) => {
            setBookingData(res.data);
        });

        setIsLoading(false);
    }


    const handleBook = (e) => {
        e.preventDefault();
        navigate(`/book`);
    };


    const handleDelete = async (e, summ) => {
        e.preventDefault();

        var result = null;
        const temp_date = `${date.getFullYear()}-${(date.getMonth() + 1) >= 10 ? `${date.getMonth() + 1}` : `0${date.getMonth() + 1}`}-${date.getDate()}`;
        const uri = `https://sgtd.onrender.com/delete-event/${temp_date}/${summ}`;
        const token = localStorage.getItem('accessToken');
        await axios({
            method: 'delete',
            url: uri,
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        }).then(async (res) => {
            result = res.data;
        });

        if (result['status']) {
            alert(`Booking deleted successfully!`);
        } else {
            alert(`Booking deleting failed!`);
        }
        window.location.reload(false);
    }


    useEffect(() => {
        handleChange();
    }, [date]);


    return (
        <div className = 'pt-20 mx-5 my-10 flex flex-col justify-center align-center'>
            {
                (position === 1) &&
                        <button className = "mb-4 w-32 rounded-md border-stone-800 border-4 px-2 py-1 self-center"
                            onClick = { (e) => handleBook(e) }
                            >Book a Date
                        </button>
            }
            <Calender changeDate = { setDate } />
            <DateDay date = { date } />
            <BookingData 
                isLoading = { isLoading } 
                data = { bookingData } 
                handleDelete = { handleDelete }
            />
        </div>
    )
}