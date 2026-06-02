import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Bell, Car, LogOut, Menu, User, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

export default function Navbar() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);

  const linkClass = ({ isActive }) =>
    isActive ? "text-red-500" : "text-gray-300 hover:text-white";

  const closeMenu = () => setOpen(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" onClick={closeMenu} className="flex items-center gap-2 text-xl font-bold">
          <img src={logo} alt="Le Vikings Cars" className="h-10 w-auto"/>
          Le_Vikings_Cars
        </Link>

        <div className="hidden items-center gap-6 lg:flex">
          <NavLink to="/" className={linkClass}>Accueil</NavLink>
          <NavLink to="/cars" className={linkClass}>Catalogue</NavLink>
          <NavLink to="/assistant" className={linkClass}>Assistant IA</NavLink>

          {user && (
            <>
              <NavLink to="/orders" className={linkClass}>Commandes</NavLink>
              <NavLink to="/addresses" className={linkClass}>Adresses</NavLink>
              <NavLink to="/tracking" className={linkClass}>Suivi</NavLink>
              <NavLink to="/notifications" className={linkClass}>
                <Bell size={18} />
              </NavLink>
            </>
          )}

          {(user?.is_staff || user?.is_superuser) && (
            <NavLink to="/dashboard" className={linkClass}>
              Dashboard
            </NavLink>
          )}
        </div>

        <div className="hidden items-center gap-4 lg:flex">
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

        <button
          onClick={() => setOpen(!open)}
          className="lg:hidden"
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="border-t border-white/10 bg-black px-6 py-5 lg:hidden">
          <div className="flex flex-col gap-4">
            <NavLink onClick={closeMenu} to="/" className={linkClass}>Accueil</NavLink>
            <NavLink onClick={closeMenu} to="/cars" className={linkClass}>Catalogue</NavLink>
            <NavLink onClick={closeMenu} to="/assistant" className={linkClass}>Assistant IA</NavLink>

            {user && (
              <>
                <NavLink onClick={closeMenu} to="/orders" className={linkClass}>Commandes</NavLink>
                <NavLink onClick={closeMenu} to="/addresses" className={linkClass}>Adresses</NavLink>
                <NavLink onClick={closeMenu} to="/tracking" className={linkClass}>Suivi</NavLink>
                <NavLink onClick={closeMenu} to="/notifications" className={linkClass}>Notifications</NavLink>
                <NavLink onClick={closeMenu} to="/profile" className={linkClass}>Profil</NavLink>
              </>
            )}

            {user?.role === "admin" && (
              <NavLink onClick={closeMenu} to="/dashboard" className={linkClass}>Dashboard</NavLink>
            )}

            {user ? (
              <button
                onClick={() => {
                  logout();
                  closeMenu();
                }}
                className="text-left text-red-500"
              >
                Déconnexion
              </button>
            ) : (
              <NavLink onClick={closeMenu} to="/login" className="text-red-500">
                Connexion
              </NavLink>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}