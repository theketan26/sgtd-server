import { useDispatch } from "react-redux"
import { logout } from "../../reducers/index";


export default function Menu() {
    const dispatch = useDispatch();


    const handleLogout = (e) => {
        e.preventDefault();
        dispatch(logout());
    }


    return (
        <div className = "absolute top-20 right-4 p-4 bg-stone-200 rounded-md font-medium">
            <div className = "text-xl">Ketan Solanki</div>
            <div className = "mt-2">ketangsolanki129@gmail.com</div>
            <div>6264255516</div>
            <button className = "mt-2 rounded-md border-stone-800 border-4 px-2 py-1"
                onClick = { (e) => handleLogout(e) }
                >Logout
            </button>
        </div>
    )
}