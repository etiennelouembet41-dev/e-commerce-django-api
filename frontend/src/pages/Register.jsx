import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await api.post("/auth/register/", form);
      navigate("/login");
    } catch {
      setError("Impossible de créer le compte.");
    }
  };

  return (
    <section className="mx-auto flex min-h-[80vh] max-w-lg items-center px-6">
      <form
        onSubmit={handleSubmit}
        className="w-full rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl"
      >
        <h1 className="text-3xl font-black">Créer un compte</h1>

        {error && (
          <div className="mt-5 rounded-xl bg-red-500/10 p-3 text-red-400">
            {error}
          </div>
        )}

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <input placeholder="Prénom" value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />
          <input placeholder="Nom" value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />
        </div>


        <input placeholder="Username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />
        <input type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />
        <input placeholder="Téléphone" value={form.phone_number} onChange={(e) => setForm({ ...form, phone_number: e.target.value })} className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />
        <input type="password" placeholder="Mot de passe" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500" />

        <button className="mt-6 w-full rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700">
          S’inscrire
        </button>

        <p className="mt-5 text-center text-gray-400">
          Déjà un compte ?{" "}
          <Link to="/login" className="text-red-500 hover:underline">
            Connexion
          </Link>
        </p>
      </form>
    </section>
  );
}