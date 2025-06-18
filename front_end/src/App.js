import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import React from 'react';
import Home from './Pages/Home/home';
import Confirma from './Pages/Confirma/confirma';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/meio" element={<Confirma />}/>
      </Routes>
    </Router>
  );
}

export default App;
