import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await login(form.email, form.password);
      navigate("/cars");
    } catch {
      setError("Email ou mot de passe incorrect.");
    }
  };

  return (
    <section className="mx-auto flex min-h-[80vh] max-w-md items-center px-6">
      <form
        onSubmit={handleSubmit}
        className="w-full rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl"
      >
        <h1 className="text-3xl font-black">Connexion</h1>
        <p className="mt-2 text-gray-400">
          Connecte-toi pour commander et suivre tes imports.
        </p>

        {error && (
          <div className="mt-5 rounded-xl bg-red-500/10 p-3 text-red-400">
            {error}
          </div>
        )}

        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="mt-6 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
        />

        <input
          type="password"
          placeholder="Mot de passe"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
        />

        <button className="mt-6 w-full rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700">
          Se connecter
        </button>

        <p className="mt-5 text-center text-gray-400">
          Pas encore de compte ?{" "}
          <Link to="/register" className="text-red-500 hover:underline">
            Créer un compte
          </Link>
        </p>
      </form>
    </section>
  );
}