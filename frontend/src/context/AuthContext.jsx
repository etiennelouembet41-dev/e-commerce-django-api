import { createContext, useState, useEffect, useContext } from "react";
import api from "../api/axios";




const AuthContext = createContext();

export function AuthProvider({ children }) {

  const [authLoading, setAuthLoading] = useState(true);

  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    const res = await api.post("/token/", { email, password });

    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);

    const profile = await api.get("/auth/profile/");
    setUser(profile.data);

    return profile.data;
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
  };

  useEffect(() => {
    const token = localStorage.getItem("access");

    if (token) {
      api.get("/auth/profile/")
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          setUser(null);
        })
        .finally(() => setAuthLoading(false));
    }
    else {
      setAuthLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, authLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}