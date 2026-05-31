import { Link, NavLink } from "react-router-dom";
import { Car, User, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Bell } from "lucide-react";

export default function Navbar() {
  const { user, logout } = useAuth();

  const linkClass = ({ isActive }) => 
    isActive ? "text-red-500" : "text-gray-300 hover:text-white";

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold">
          <Car className="text-red-500" />
          Le Vikings Cars
        </Link>

        <div className="hidden items-center gap-6 md:flex">
          <NavLink to="/" className={linkClass}>Accueil</NavLink>
          <NavLink to="/cars" className={linkClass}>Catalogue</NavLink>
          <NavLink to="/assistant" className={linkClass}>Assistant IA</NavLink>
          <NavLink to="/tracking" className={linkClass}>Suivi</NavLink>
          <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
          <NavLink to="/notifications" className={linkClass}> <Bell size={18} /> </NavLink>
          <NavLink to="/addresses" className={linkClass}> Adresses</NavLink>
          <NavLink to="/orders" className={linkClass}>Commandes</NavLink>
        </div>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link to="/profile" className="flex items-center gap-2 text-gray-300">
                <User size={18} />
                {user.first_name || user.username}
              </Link>
              <button onClick={logout} className="text-gray-300 hover:text-red-500">
                <LogOut size={20} />
              </button>
            </>
          ) : (
            <Link
              to="/login"
              className="rounded-full bg-red-600 px-5 py-2 font-semibold hover:bg-red-700"
            >
              Connexion
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}