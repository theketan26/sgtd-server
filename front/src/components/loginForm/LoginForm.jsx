import axios from "axios";
import { useState } from "react"


export default function() {
    const [note, setNote] = useState('');
    const [number, setNumber] = useState('');
    const [password, setPassword] = useState('');


    const checkNumber = () => {
        let num = Number(number);
        if (num > 6000000000 && num < 9999999999) {
            return true;
        } else {
            setNote('Invalid number!');
            return false;
        }
    };


    const checkPassword = () => {
        if (password.length >= 8) {
            return true;
        } else {
            setNote('Invalid password!');
            return false;
        }
    }


    const handleSubmit = async (e) => {
        setNote('Loading');

        e.preventDefault();
        if (!(checkNumber() && checkPassword())) return

        let uri = `https://sgtd.onrender.com/login`;
        let formData = new FormData();
        formData.append('username', number);
        formData.append('password', password);

        let data;
        await axios({
            method: 'post',
            url: uri,
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            data: formData
        }).then(async (res) => {
            data = res.data;
        });

        console.log(data);
        if (data.status) {
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('position', 0);
            setNote('');
        } else {
            setNote(data.message);
        }
    };


    return (
        <div className = "">
            <div className = "text-3xl font-bold text-center">
                Login
            </div>
            <form className = "mt-10">
                <div className = "flex justify-between">
                    <label for = 'number'>Number</label>
                    <input type="text" name="number" placeholder = "Enter your number..." 
                        value = { number } onChange = { (e) => setNumber(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>
                <div className = "mt-2 flex justify-between">
                    <label for = 'password'>Password</label>
                    <input type = "password" name="password" placeholder = "Enter your password..." 
                        value = { password } onChange = { (e) => setPassword(e.target.value) }
                        className = "ms-5 border-2 border-stone-600 px-2 py-1 rounded-md" 
                    />
                </div>
                <div className = "mt-5 flex flex-col">
                    <button onClick = { handleSubmit }
                        className = "px-5 py-2 font-bold rounded-md bg-stone-300 self-center"
                    >
                        Login
                    </button>
                </div>
                <div className = "mt-5 text-center text-rose-700">
                    { note }
                </div>
                <div className = "mt-5 text-center">
                    Don't have accout click here!
                </div>
            </form>
        </div>
    )
}