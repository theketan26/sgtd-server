export default function (props) {
    const months_english = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const months_hindi = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितम्बर", "अक्टूबर", "नवंबर", "दिसंबर"];
    const days_english = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const days_hindi = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरूवार", "शुक्रवार", "शनिवार"];


    return (
        <div className = 'mt-10 flex flex-col self-center'>
            <div className = 'text-3xl font-medium'>
                { props.date.getDate() } / { props.date.getMonth() + 1 } / { props.date.getFullYear() }
            </div>

            <div className = 'mt-5 text-l'>
                { days_english[props.date.getDay()] }, { months_english[props.date.getMonth()] }
            </div>

            <div className = 'mt-2 text-l'>
                { days_hindi[props.date.getDay()] }, { months_hindi[props.date.getMonth()] }
            </div>
        </div>
    )
}