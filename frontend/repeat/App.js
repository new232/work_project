import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Order from "./pages/Order";
import Location from "./pages/Location";
import Basket from "./pages/Basket";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/order" element={<Order />} />
        <Route path="/location" element={<Location />} /> {/* ✅ 추가 */}
         <Route path="/basket" element={<Basket />} />
      </Routes>
    </Router>
  );
}

export default App;

