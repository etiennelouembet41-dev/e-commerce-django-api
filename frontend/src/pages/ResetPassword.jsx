import { useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import api from "../api/axios";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const uid = searchParams.get("uid");
  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const res = await api.post("/auth/reset-password/", {
        uid,
        token,
        new_password: newPassword,
      });

      setMessage(res.data.message);
      setNewPassword("");
    } catch (err) {
      setError(err.response?.data?.error || "Lien invalide ou expiré.");
    }
  };

  return (
    <section className="mx-auto flex min-h-[80vh] max-w-md items-center px-6">
      <form onSubmit={handleSubmit} className="w-full rounded-3xl border border-white/10 bg-white/5 p-8">
        <h1 className="text-3xl font-black">Nouveau mot de passe</h1>

        {!uid || !token ? (
          <div className="mt-5 rounded-xl bg-red-500/10 p-3 text-red-400">
            Lien de réinitialisation invalide.
          </div>
        ) : (
          <>
            {message && (
              <div className="mt-5 rounded-xl bg-green-500/10 p-3 text-green-400">
                {message}{" "}
                <Link to="/login" className="underline">
                  Se connecter
                </Link>
              </div>
            )}

            {error && (
              <div className="mt-5 rounded-xl bg-red-500/10 p-3 text-red-400">
                {error}
              </div>
            )}

            <input
              type="password"
              placeholder="Nouveau mot de passe"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="mt-6 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 outline-none focus:border-red-500"
              required
            />

            <button className="mt-6 w-full rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700">
              Réinitialiser
            </button>
          </>
        )}
      </form>
    </section>
  );
}