import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { Provider } from 'react-redux';
import './index.css';
import { login, logout } from './actions/actions';
import store from './store';


import Home from './home/Home';
import Login from './login/Login';
import Register from './register/Register';


const App = () => {
    const isLoggedIn = useSelector((state) => state.isLoggedIn);
	const dispatch = useDispatch();


	return (
			<Router>
				<Routes>
					{ isLoggedIn ? (
							<></>
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
	<Provider store={store}>
		<React.StrictMode>
			<App />
		</React.StrictMode>
	</Provider>
);