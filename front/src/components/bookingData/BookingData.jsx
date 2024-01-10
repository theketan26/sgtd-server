import { useEffect, useState } from "react"

export default function (props) {
    const [isBook, setIsBook] = useState(false);


    useEffect(() => {
        try {
            if (props.data['message'].length > 0) {
                setIsBook(true);
            }
            else {
                setIsBook(false);
            }
        } catch (e) {
        }
    }, [props])


    return (
        <div className = "self-center mt-10 p-5 text-xl font-bold">
            { props.isLoading ? 
                <div>
                    Loading
                </div>
                :
                <div>
                    { isBook ? 
                        <div className = "flex flex-col align-center">
                            <div className = "bg-rose-300 text-center">Booked</div>
                            <button className = "mt-5 px-3 py-1 border-4">Check</button>
                        </div>
                        :
                        <div className = "bg-green-300">
                            No Bookings
                        </div>
                    }
                </div>
            }
        </div>
    )
}