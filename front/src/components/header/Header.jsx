import { useSelector } from "react-redux";
import { FaUser, FaRegUser } from "react-icons/fa";
import { useEffect, useState } from "react";


import Menu from './Menu';


export default function Header() {
    const isLoggedIn = useSelector((state) => state.isLoggedIn);
    const [loginOver, setLoginOver] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [data, setData] = useState({});


    useEffect(() => {
        setData(JSON.parse(localStorage.getItem('userData')));
        console.log(data);
    }, []);


    return (
        <div>
            <div className="absolute top-0 left-0 w-screen bg-orange-300 px-10 py-5 text-xl font-medium flex justify-between">
                <span>Shree Guru Tekchand Dharamshala</span>
                <div className = "cursor-pointer"
                    onMouseOver = { () => setLoginOver(true) }
                    onMouseOut = { () => setLoginOver(false) }
                    onClick = { () => setShowMenu(!showMenu) }
                    >
                    {
                        loginOver ? <FaUser /> : <FaRegUser />
                    }
                </div>
            </div>
            {
                showMenu && <Menu data = { data } />
            }
        </div>
    )
}