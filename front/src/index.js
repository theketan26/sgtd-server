import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import { Provider } from 'react-redux';
import store from './store';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { login, logout, setPosition0, setPosition1 } from './reducers/index';


import Home from './home/Home';
import Login from './login/Login';
import Register from './register/Register';
import Book from './book/Book';


const App = () => {
	const isLoggedIn = useSelector((state) => state.isLoggedIn);
	const position = useSelector((state) => state.position);
	const dispatch = useDispatch();


	const checkLogin = async () => {
		let temp = localStorage.getItem('accessToken');

		if (typeof(temp) == 'string') {
			dispatch(login());
		} else {
			dispatch(logout());
		}

		let data = JSON.parse(localStorage.getItem('userData'));
		try {
			if (data['position'] == 1) {
				dispatch(setPosition1());
			} else {
				dispatch(setPosition0());
			}
		} catch (e) {
            dispatch(setPosition0());
        }
	};


	useEffect(() => {
		checkLogin();
	}, [isLoggedIn, position]);


	return (
			<Router>
				<Routes>
					{ isLoggedIn ? (
							<>
								{
									(position === 1) &&
										<Route path = "/register" element = { <Register /> } />
								}
								<Route path = "/book" element = { <Book /> } />
							</> 
						) : (
							<>
								<Route path="/login" element = { <Login /> } />
							</>
						)
					}
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