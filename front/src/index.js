import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import { Provider } from 'react-redux';
import store from './store';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { login, logout } from './reducers/index';


import Home from './home/Home';
import Login from './login/Login';
import Register from './register/Register';


const App = () => {
	const isLoggedIn = useSelector((state) => state.isLoggedIn);
	const dispatch = useDispatch();


	const checkLogin = async () => {
		let temp = localStorage.getItem('accessToken');
		if (typeof(temp) == 'string') {
			dispatch(login());
		} else {
			dispatch(logout());
		}
	};


	useEffect(() => {
		checkLogin();
	}, [isLoggedIn]);


	return (
			<Router>
				<Routes>
					{ isLoggedIn ? (
							<>
								<Route path="/protected" element = { <h1>Hello world</h1> } />
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
	<Provider store = { store }>
		<React.StrictMode>
			<App />
		</React.StrictMode>
	</Provider>
);