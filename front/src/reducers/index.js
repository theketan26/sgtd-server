import { createSlice } from '@reduxjs/toolkit';


const initialState = {
    isLoggedIn: false,
    position: 0
};


const loginSlice = createSlice({
    name: 'login',
    initialState,
    reducers: {
        login: (state, action) => {
            state.isLoggedIn = true;
        },
        logout: (state, action) => {
            state.isLoggedIn = false;
        },
        setPosition1: (state, action) => {
            state.position = 1;
        },
        setPosition0: (state, action) => {
            state.position = 0;
        },
    },
});


export const { login, logout, setPosition0, setPosition1 } = loginSlice.actions;
export default loginSlice.reducer;