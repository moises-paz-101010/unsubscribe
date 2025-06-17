import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import React from 'react';
import Home from './Pages/home';
import Confirma from './Pages/confirma';

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
