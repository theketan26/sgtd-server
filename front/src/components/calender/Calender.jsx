import { Calendar } from 'react-calendar';
import 'react-calendar/dist/Calendar.css';


export default function(props) {
    return (
        <div className = "self-center">
            <Calendar className = 'font-bold' onChange = { props.changeDate } value = { props.date } />
        </div>
    )
}