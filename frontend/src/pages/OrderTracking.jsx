import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import api from "../api/axios";
import ImportTimeline from "../components/ImportTimeline";
import Loader from "../components/Loader";

export default function OrderTracking() {
  const [searchParams] = useSearchParams();
  const initialOrderId = searchParams.get("order") || "";

  const [orderId, setOrderId] = useState(initialOrderId);
  const [tracking, setTracking] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchTracking = async (customOrderId = orderId) => {
    if (!customOrderId) {
      setError("Veuillez entrer un numéro de commande.");
      return;
    }

    setLoading(true);
    setError("");
    setTracking(null);

    try {
      const res = await api.get(`/imports/tracking/${customOrderId}/`);
      setTracking(res.data);
    } catch (err) {
      console.error(err);
      setError("Commande introuvable ou accès non autorisé.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialOrderId) {
      fetchTracking(initialOrderId);
    }
  }, [initialOrderId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchTracking(orderId);
  };

  return (
    <section className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-4xl font-black">Suivi import</h1>

      <form onSubmit={handleSubmit} className="mt-8 flex gap-3">
        <input
          value={orderId}
          onChange={(e) => setOrderId(e.target.value)}
          placeholder="Numéro de commande"
          className="flex-1 rounded-2xl border border-white/10 bg-black px-5 py-4 outline-none focus:border-red-500"
        />

        <button className="rounded-2xl bg-red-600 px-6 font-black hover:bg-red-700">
          <Search />
        </button>
      </form>

      {error && (
        <div className="mt-6 rounded-xl bg-red-500/10 p-4 text-red-400">
          {error}
        </div>
      )}

      {loading && <Loader />}

      {!tracking && !error && !loading && (
        <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-8 text-gray-400">
          Entrez votre numéro de commande pour voir le suivi d’importation.
        </div>
      )}

      {tracking && !loading && (
        <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-8">
          <p className="text-sm text-gray-400">Commande #{tracking.order_id}</p>

          <h2 className="mt-1 text-2xl font-bold">{tracking.car}</h2>

          <p className="mt-2 text-gray-400">
            Livraison : {tracking.delivery_city}
          </p>

          <div className="mt-8">
            <ImportTimeline timeline={tracking.timeline} />
          </div>

          <p className="mt-8 text-gray-400">
            Délai estimé : {tracking.estimated_import_days} jours
          </p>
        </div>
      )}
    </section>
  );
}