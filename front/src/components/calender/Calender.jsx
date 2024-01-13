import { Calendar } from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { useState } from 'react';


export default function(props) {
    const [selectedDates, setSelectedDates] = useState([new Date('2024-01-10'), new Date('2024-01-15')]);

    
    const tileContent = ({ date, view }) => {
        if (view === 'month' && selectedDates.find(selectedDate => selectedDate.toDateString() === date.toDateString())) {
            return <span style={{ backgroundColor: 'red', borderRadius: '50%', display: 'block' }}></span>;
        }
        return null;
    };


    return (
        <div className = "self-center">
            <Calendar 
                tileContent = { tileContent }
                className = 'font-bold' 
                onChange = { props.changeDate } 
                value = { props.date } 
            />
        </div>
    )
}