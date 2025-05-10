import './App.css'

import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useDispatch } from 'react-redux';
import { setAuthenticated } from './slices/authSlice';

import RegisterForm from './Pages/RegisterForm/RegisterForm';
import Login from './Pages/Login/Login';
import Home from './Pages/Home/Home';
import NavTop from './Components/NavTop/NavTop';

import PrivateRoute from './routes/PrivateRoute';


function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) dispatch(setAuthenticated(true));
  }, [dispatch]);

  return (
    <>
      <div>
        <NavTop></NavTop>
      </div>
      <div>
        <BrowserRouter>
          <Routes>
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/login" element={<Login />} />
            <Route path="/home" element={
              // <PrivateRoute>
                <Home />
              // </PrivateRoute>
            } />
            <Route path="*" element={<Login />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
