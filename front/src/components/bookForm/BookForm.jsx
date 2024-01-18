import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function() {
    const summaries = ['marriage', 'birthday', 'surajpuja', 'uthawna'];
    const [note, setNote] = useState('');
    const [date, setDate] = useState(new Date());
    const [summary, setSummary] = useState('marrige');
    const [hostName, setHostName] = useState('');
    const [hostNumber, setHostNumber] = useState(0);
    const [hostEmail, setHostEmail] = useState('');
    const [hostAddress, setHostAddress] = useState('');
    const navigate = useNavigate();


    const checkDate = () => {
        let temp_date = new Date(date);
        if (temp_date > new Date()) {
            return true;
        } else {
            setNote('Invalid date!');
            return false;
        }
    }


    const checkHostName = () => {
        if (hostName.length >= 3) {
            return true;
        } else {
            setNote('Invalid host name!');
            return false;
        }
    }


    const checkHostNumber = () => {
        let num = Number(hostNumber);
        if (num > 6000000000 && num < 9999999999) {
            return true;
        } else {
            setNote('Invalid host number!');
            return false;
        }
    }


    const checkHostAddress = () => {
        if (hostAddress.length >= 3) {
            return true;
        } else {
            setNote('Invalid host address!');
            return false;
        }
    }


    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!(checkDate() && checkHostName() && checkHostNumber() && checkHostAddress())) {
            return;
        }

        setNote('');

        var result = null;
        const uri = `https://sgtd.onrender.com/add-event/${date}`;
        const token = localStorage.getItem('accessToken');
        await axios({
            method: 'post',
            url: uri,
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `Bearer ${token}`,
            data: {
                'summary': summary,
                'description': {
                    'host_name': hostName,
                    'host_number': hostNumber,
                    'host_email': hostEmail,
                    'host_address': hostAddress,
                    'booker_name': '',
                    'booker_number': 0,
                    'dates': [date],
                    'days': 1
                },
                'location': ''
            }
        }).then(async (res) => {
            result = res;
        });

        console.log(result);
    };


    return (
        <div className = "">
            <div className = "text-3xl font-bold text-center">
                Book a Date
            </div>
            <form className = "mt-10">
                <div className = "flex justify-between">
                    <label for = 'date'>Date</label>
                    <input type = "date" name = "date"
                        value = { date } onChange = { (e) => setDate(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>

                <div className = "mt-2 flex justify-between">
                    <label for = 'summary'>Summary</label>
                    <select className = "px-4 py-2"
                        onChange = { (e) => setSummary(e.target.value) }
                        value = { summary }
                    >
                        {
                            summaries.map((sum) => {
                                return (
                                    <option key = { sum } value = { sum }>
                                        { sum.toLocaleUpperCase() }
                                    </option>
                                )
                            })
                        }
                    </select>
                </div>

                <div className = "mt-2 flex justify-between">
                    <label for = 'host_name'>Host Name</label>
                    <input type = "text" name = "host_name" placeholder = "Enter name of host..." 
                        value = { hostName } onChange = { (e) => setHostName(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>

                <div className = "mt-2 flex justify-between">
                    <label for = 'host_number'>Host Number</label>
                    <input type = "number" name = "host_number" placeholder = "Enter number of host..." 
                        value = { hostNumber } onChange = { (e) => setHostNumber(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>

                <div className = "mt-2 flex justify-between">
                    <label for = 'host_email'>Host Email</label>
                    <input type = "email" name = "host_email" placeholder = "Enter email of host..." 
                        value = { hostEmail } onChange = { (e) => setHostEmail(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>

                <div className = "mt-2 flex justify-between">
                    <label for = 'host_address'>Host Address</label>
                    <input type = "text" name = "host_address" placeholder = "Enter address of host..." 
                        value = { hostAddress } onChange = { (e) => setHostAddress(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>

                <div className = "mt-5 flex flex-col">
                    <button onClick = { handleSubmit }
                        className = "px-5 py-2 font-bold rounded-md bg-stone-300 self-center"
                    >
                        Book
                    </button>
                </div>

                <div className = "mt-5 text-center text-rose-700">
                    { note }
                </div>
            </form>
        </div>
    )
}