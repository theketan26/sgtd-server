import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';


import Home from './home/Home';
import Login from './login/Login';
import Register from './register/Register';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render( 
	<React.StrictMode >
		{/* <Home /> */}
		{/* <Login /> */}
		<Register /> 
	</ React.StrictMode>
);