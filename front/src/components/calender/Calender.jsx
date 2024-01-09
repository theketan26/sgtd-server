import { useEffect, useState } from 'react';
import { Calendar } from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import axios from 'axios';


export default function() {
    const months_english = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const months_hindi = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितम्बर", "अक्टूबर", "नवंबर", "दिसंबर"];
    const days_english = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const days_hindi = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरूवार", "शुक्रवार", "शनिवार"];


    const [date, setDate] = useState(new Date());
    const [bookingData, setBookingData] = useState({});


    const handleChange = () => {
        let uri = `https://miniature-winner-rjvw7r949635rjg-8000.app.github.dev/get-events/${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}/1`;
        axios({
            method: 'get',
            url: uri,
        }).then(async (res) => {
            await setBookingData(res.data);
            console.log(bookingData);
        });
    }


    useEffect(() => {
        handleChange();
    }, [date]);


    return (
        <div className = "mx-40 my-20 flex flex-col">
            <Calendar className = 'self-center font-bold' onChange = { setDate } value = { date } />

            <div className = 'mt-10 self-center flex flex-col'>
                <div className = 'text-5xl font-medium'>
                    { date.getDate() } / { date.getMonth() + 1 } / { date.getFullYear() }
                </div>

                <div className = 'mt-5 text-2xl'>
                    { days_english[date.getDay()] }, { months_english[date.getMonth()] }
                </div>

                <div className = 'mt-2 text-2xl'>
                    { days_hindi[date.getDay()] }, { months_hindi[date.getMonth()] }
                </div>
            </div>

            <div className = 'self-center'>
                { bookingData.status ? <div>Yes</div> : <div>No</div>}
            </div>
        </div>
    )
}