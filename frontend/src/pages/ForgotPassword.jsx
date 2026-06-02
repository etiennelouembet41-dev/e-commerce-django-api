import { useState } from "react";
import api from "../api/axios";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const res = await api.post("/auth/forgot-password/", { email });
      setMessage(res.data.message);
      setEmail("");
    } catch {
      setError("Impossible d’envoyer l’email de réinitialisation.");
    }
  };

  return (
    <section className="mx-auto flex min-h-[80vh] max-w-md items-center px-6">
      <form onSubmit={handleSubmit} className="w-full rounded-3xl border border-white/10 bg-white/5 p-8">
        <h1 className="text-3xl font-black">Mot de passe oublié</h1>
        <p className="mt-2 text-gray-400">
          Entrez votre email pour recevoir un lien de réinitialisation.
        </p>

        {message && <div className="mt-5 rounded-xl bg-green-500/10 p-3 text-green-400">{message}</div>}
        {error && <div className="mt-5 rounded-xl bg-red-500/10 p-3 text-red-400">{error}</div>}

        <input
          type="email"
          placeholder="Votre email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-6 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
          required
        />

        <button className="mt-6 w-full rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700">
          Envoyer le lien
        </button>
      </form>
    </section>
  );
}