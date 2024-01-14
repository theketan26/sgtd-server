import { createSlice } from '@reduxjs/toolkit';


const initialState = {
    isLoggedIn: false,
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
    },
});


export const { login, logout } = loginSlice.actions;
export default loginSlice.reducer;