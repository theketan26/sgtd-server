import axios from 'axios';


export default function async (date, to) {
    const url = `https://miniature-winner-rjvw7r949635rjg-8000.app.github.dev/get-events/${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}/${to}`
    // axios.get(url).then((res) => {
    //     console.log(res);
    // })
    axios({
        method: 'get',
        url: `url`
    }).then((res) => {
        console.log(res);
    });
    // console.log(date.getDate());
}