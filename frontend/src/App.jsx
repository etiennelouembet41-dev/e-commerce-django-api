import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Cars from "./pages/Cars";
import CarDetail from "./pages/CarDetail";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Assistant from "./pages/Assistant";
import OrderTracking from "./pages/OrderTracking";
import AdminDashboard from "./pages/AdminDashboard";
import Checkout from "./pages/Checkout";

export default function App() {
  return (
    <div className="min-h-screen bg-[#050505] text-white">
      <Navbar />
 
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cars" element={<Cars />} />
        <Route path="/cars/:id" element={<CarDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/assistant" element={<Assistant />} /> 
        <Route path="/tracking" element={<OrderTracking />} />
        <Route path="/dashboard" element={<AdminDashboard />} />
        <Route path="/checkout/:carId" element={<Checkout />} />
      </Routes>
    </div>
  );
}