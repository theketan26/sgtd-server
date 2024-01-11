import RegisterForm from "../components/loginForm/RegisterForm"


export default function () {
    return (
        <div className = "w-screen h-screen grid place-content-center bg-orange-100 text-stone-800">
            <div className = "p-10 border-4 rounded-xl border-stone-600">
                <RegisterForm />
            </div>
        </div>
    )
}