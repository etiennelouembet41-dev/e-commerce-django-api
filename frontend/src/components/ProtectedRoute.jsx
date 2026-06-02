import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Loader from "./Loader";

export default function ProtectedRoute({ children, adminOnly = false }) {
  const { user, authLoading } = useAuth();

  if (authLoading) {
    return <Loader />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user.is_staff && !user.is_superuser) {
    return <Navigate to="/" replace />;
  }

  return children;
}