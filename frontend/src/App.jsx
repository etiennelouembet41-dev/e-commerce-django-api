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
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import Notifications from "./pages/Notifications";
import ProtectedRoute from "./components/ProtectedRoute";
import Addresses from "./pages/Addresses";
import Orders from "./pages/Orders";
import OrderDetail from "./pages/OrderDetail";
import NotFound from "./pages/NotFound";
import Footer from "./components/Footer";


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
        <Route path="/payment-success" element={<PaymentSuccess />} />
        <Route path="/payment-cancel" element={<PaymentCancel />} />  
        <Route path="/notifications"  element={<Notifications />} />
        <Route path="/profile" element={<ProtectedRoute> <Profile /></ProtectedRoute>}/>
        <Route path="/checkout/:carId" element={<ProtectedRoute><Checkout /></ProtectedRoute>}/>
        <Route path="/tracking" element={<ProtectedRoute><OrderTracking /></ProtectedRoute>}/>
        <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>}/>
        <Route path="/dashboard" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>}/>
        <Route path="/addresses" element={<ProtectedRoute><Addresses /></ProtectedRoute>}/>
        <Route path="/orders"element={<ProtectedRoute><Orders /></ProtectedRoute>}/>
        <Route path="/orders/:id"element={<ProtectedRoute><OrderDetail /></ProtectedRoute>}/>
        <Route path="*" element={<NotFound />} />
        


      </Routes>

      <Footer />
        
    </div>
  );
}