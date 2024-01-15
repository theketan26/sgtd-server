import { useDispatch, useSelector } from "react-redux"
import { logout } from "../../reducers/index";
import { useNavigate } from "react-router-dom";


export default function Menu(props) {
    const isLoggedIn = useSelector((state) => state.isLoggedIn);
    const dispatch = useDispatch();
    const navigate = useNavigate();


    const handleLogout = (e) => {
        e.preventDefault();
        dispatch(logout());
        localStorage.clear();
    }


    const handleLogin = (e) => {
        e.preventDefault();
        navigate('/login');
    }


    return (
        <div className = "absolute top-20 right-4 p-4 bg-stone-200 rounded-md font-medium">
            {
                isLoggedIn ? 
                    <div>
                        <div className = "text-xl">{ props.data.name }</div>
                        <div className = "mt-2">{ props.data.email }</div>
                        <div>{ props.data.number }</div>
                        <button className = "mt-2 rounded-md border-stone-800 border-4 px-2 py-1"
                            onClick = { (e) => handleLogout(e) }
                            >Logout
                        </button>
                    </div>
                    :
                    <div>
                        <div>Not logged in!</div>
                        <button className = "mt-2 rounded-md border-stone-800 border-4 px-2 py-1"
                            onClick = { (e) => handleLogin(e) }
                            >Login
                        </button>
                    </div>
            }
        </div>
    )
}