import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Profile() {
  const navigate = useNavigate();

  const [form, setForm] = useState(null);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access");

        if (!token) {
          navigate("/login");
          return;
        }

        const res = await api.get("/auth/profile/");
        setForm(res.data);
      } catch (err) {
        console.log("PROFILE ERROR:", err.response?.status, err.response?.data);
        setError("Impossible de charger le profil. Connecte-toi à nouveau.");
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaved(false);

    try {
      const res = await api.patch("/auth/profile/", form);
      setForm(res.data);
      setSaved(true);
    } catch (err) {
      console.log("UPDATE PROFILE ERROR:", err.response?.data);
      setError("Impossible de mettre à jour le profil.");
    }
  };

  if (error) {
    return (
      <div className="p-6 text-red-400">
        {error}
      </div>
    );
  }

  if (!form) {
    return <div className="p-6 text-gray-400">Chargement...</div>;
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <div className="rounded-3xl border border-white/10 bg-white/5 p-8">
        <h1 className="text-3xl font-black">Mon profil</h1>

        {saved && (
          <div className="mt-5 rounded-xl bg-green-500/10 p-3 text-green-400">
            Profil mis à jour.
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-8 grid gap-4">
          <input
            value={form.email || ""}
            disabled
            className="rounded-2xl border border-white/10 bg-black/60 px-4 py-3 text-gray-400"
          />

          <input
            value={form.first_name || ""}
            onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            placeholder="Prénom"
            className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
          />

          <input
            value={form.last_name || ""}
            onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            placeholder="Nom"
            className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
          />

          <input
            value={form.phone_number || ""}
            onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
            placeholder="Téléphone"
            className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
          />

          <input
            value={form.city || ""}
            onChange={(e) => setForm({ ...form, city: e.target.value })}
            placeholder="Ville"
            className="rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
          />

          <button className="rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700">
            Enregistrer
          </button>
        </form>
      </div>
    </section>
  );
}