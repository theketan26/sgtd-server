import LoginForm from "../components/loginForm/LoginForm"


export default function () {
    return (
        <div className = "w-screen h-screen grid place-content-center bg-orange-100 text-stone-800">
            <div className = "p-10 border-4 rounded-xl border-stone-600">
                <LoginForm />
            </div>
        </div>
    )
}