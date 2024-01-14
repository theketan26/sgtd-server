import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';


import Home from './home/Home';
import Login from './login/Login';
import Register from './register/Register';


const App = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);


	const checkLogin = async () => {
		let temp = localStorage.getItem('accessToken');
		await setIsLoggedIn(typeof(temp) == 'string');
	};


	useEffect(() => {
		checkLogin();
	}, [isLoggedIn]);


	return (
			<Router>
				<Routes>
					{ isLoggedIn ? (
							<>
								<Route path="/protected" element = { { isLoggedIn } } />
							</>
						) : (
							<>
								<Route path="/login" element = { <Login /> } />
								<Route path="/register" element = { <Register /> } />
							</>
					)}
					<Route path="/" element = { <Home /> } />
				</Routes>
			</Router>
	);
};


const root = createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<App />
	</React.StrictMode>
);