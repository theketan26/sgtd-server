import Header from "../components/header/Header";
import BookForm from "../components/bookForm/BookForm";


export default function () {
    return (
        <div>
            <Header />
            <div className = "w-screen min-h-screen grid place-content-center bg-orange-100 text-stone-800">
                <div className = "p-10 border-4 rounded-xl border-stone-600">
                    <BookForm />
                </div>
            </div>
        </div>
    )
}