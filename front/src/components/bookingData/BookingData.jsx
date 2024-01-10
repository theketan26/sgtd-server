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
                        <div className = "bg-rose-300">
                            Booked
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