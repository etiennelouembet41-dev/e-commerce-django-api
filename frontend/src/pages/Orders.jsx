import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { CreditCard, MapPin, PackageSearch } from "lucide-react";
import api from "../api/axios";

export default function Orders() {
  const [orders, setOrders] = useState([]);

  const payOrder = async (orderId, paymentType = "deposit") => {
    try {
      const res = await api.post("/payments/create-checkout-session/", {
        order_id: orderId,
        payment_type: paymentType,
      });

      window.location.href = res.data.checkout_url;
    } catch {
      alert("Impossible de lancer le paiement.");
    }
  };

  useEffect(() => {
    api.get("/orders/").then((res) => {
      setOrders(res.data.results || res.data);
    });
  }, []);

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <p className="text-sm font-bold uppercase text-red-500">Espace client</p>
      <h1 className="mt-2 text-4xl font-black">Mes commandes</h1>

      <div className="mt-8 grid gap-5">
        {orders.map((order) => (
          <div
            key={order.id}
            className="rounded-3xl border border-white/10 bg-white/5 p-6"
          >
            <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
              <div>
                <p className="text-sm text-gray-400">Commande #{order.id}</p>

                <h2 className="mt-1 text-2xl font-bold">
                  {order.car_name || `Voiture #${order.car}`}
                </h2>

                <div className="mt-4 flex flex-wrap gap-3">
                  <Badge value={order.status} />
                  <Badge value={order.payment_status} />
                </div>

                <div className="mt-4 flex flex-wrap gap-5 text-gray-400">
                  <span className="flex items-center gap-2">
                    <CreditCard size={18} />
                    {Number(order.total_price || 0).toLocaleString()} MYR
                  </span>

                  <span className="flex items-center gap-2">
                    <MapPin size={18} />
                    {order.delivery_city_name || `Ville #${order.delivery_city}`}
                  </span>

                  {order.import_status && (
                    <span className="flex items-center gap-2">
                      <PackageSearch size={18} />
                      Import : {order.import_status}
                    </span>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                {order.payment_status === "unpaid" && (
                  <button
                    onClick={() => payOrder(order.id)}
                    className="rounded-2xl border border-red-500 px-5 py-3 font-bold text-red-500 transition hover:bg-red-500 hover:text-white"
                  >
                    Payer l’acompte
                  </button>
                )}

                <Link
                  to={`/tracking?order=${order.id}`}
                  className="rounded-2xl bg-red-600 px-5 py-3 text-center font-bold transition hover:bg-red-700"
                >
                  Suivre import
                </Link>
              </div>
            </div>
          </div>
        ))}

        {orders.length === 0 && (
          <div className="rounded-3xl border border-white/10 bg-white/5 p-8 text-gray-400">
            Aucune commande pour le moment.
          </div>
        )}
      </div>
    </section>
  );
}

function Badge({ value }) {
  const colors = {
    unpaid: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    deposit_paid: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    paid: "bg-green-500/10 text-green-400 border-green-500/20",
    confirmed: "bg-green-500/10 text-green-400 border-green-500/20",
    pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    cancelled: "bg-red-500/10 text-red-400 border-red-500/20",
    completed: "bg-green-500/10 text-green-400 border-green-500/20",
  };

  return (
    <span
      className={`rounded-full border px-3 py-1 text-sm font-bold ${
        colors[value] || "border-white/10 bg-white/5 text-gray-300"
      }`}
    >
      {value}
    </span>
  );
}