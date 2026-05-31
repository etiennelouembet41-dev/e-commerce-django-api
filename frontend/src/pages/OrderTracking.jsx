import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { CheckCircle, Circle, Search } from "lucide-react";
import api from "../api/axios";

export default function OrderTracking() {
  const [searchParams] = useSearchParams();
  const initialOrderId = searchParams.get("order") || "";

  const [orderId, setOrderId] = useState(initialOrderId);
  const [tracking, setTracking] = useState(null);
  const [error, setError] = useState("");

  const fetchTracking = async (customOrderId = orderId) => {
    if (!customOrderId) return;

    setError("");
    setTracking(null);

    try {
      const res = await api.get(`/imports/tracking/${customOrderId}/`);
      setTracking(res.data);
    } catch {
      setError("Commande introuvable ou accès non autorisé.");
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

      {tracking && (
        <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-8">
          <p className="text-sm text-gray-400">Commande #{tracking.order_id}</p>

          <h2 className="mt-1 text-2xl font-bold">{tracking.car}</h2>

          <p className="mt-2 text-gray-400">
            Livraison : {tracking.delivery_city}
          </p>

          <div className="mt-8 space-y-5">
            {tracking.timeline.map((step) => (
              <div key={step.status} className="flex items-center gap-4">
                {step.completed ? (
                  <CheckCircle className="text-green-500" />
                ) : (
                  <Circle className="text-gray-500" />
                )}

                <div>
                  <p
                    className={
                      step.current
                        ? "font-bold text-red-500"
                        : "font-semibold text-gray-300"
                    }
                  >
                    {step.status}
                  </p>

                  {step.current && (
                    <p className="text-sm text-gray-400">Étape actuelle</p>
                  )}
                </div>
              </div>
            ))}
          </div>

          <p className="mt-8 text-gray-400">
            Délai estimé : {tracking.estimated_import_days} jours
          </p>
        </div>
      )}
    </section>
  );
}