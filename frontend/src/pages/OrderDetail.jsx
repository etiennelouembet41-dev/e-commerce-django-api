import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { CreditCard, MapPin, PackageSearch } from "lucide-react";
import api from "../api/axios";
import StatusBadge from "../components/StatusBadge";
import Loader from "../components/Loader";

export default function OrderDetail() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    api.get(`/orders_order/${id}/`).then((res) => setOrder(res.data));
  }, [id]);

  const payOrder = async () => {
    const res = await api.post("/payments/create_checkout_session/", {
      order_id: order.id,
      payment_type: "deposit",
    });

    window.location.href = res.data.checkout_url;
  };

  if (!order) {
    return <Loader />;
  }

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <p className="text-sm font-bold uppercase text-red-500">
        Commande #{order.id}
      </p>

      <h1 className="mt-2 text-4xl font-black">
        {order.car_name || `Voiture #${order.car}`}
      </h1>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-2xl font-bold">Résumé</h2>

          <div className="mt-6 space-y-4 text-gray-300">
            <Info
              icon={<CreditCard />}
              label="Statut paiement"
              value={<StatusBadge value={order.payment_status} />}
            />

            <Info
              icon={<PackageSearch />}
              label="Statut commande"
              value={<StatusBadge value={order.status} />}
            />

            <Info
              icon={<PackageSearch />}
              label="Statut import"
              value={
                order.import_status ? (
                  <StatusBadge value={order.import_status} />
                ) : (
                  "Non défini"
                )
              }
            />

            <Info
              icon={<MapPin />}
              label="Ville livraison"
              value={order.delivery_city_name || `#${order.delivery_city}`}
            />
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            {order.payment_status === "unpaid" && (
              <button
                onClick={payOrder}
                className="rounded-2xl bg-red-600 px-5 py-3 font-bold hover:bg-red-700"
              >
                Payer l’acompte
              </button>
            )}

            <Link
              to={`/tracking?order=${order.id}`}
              className="rounded-2xl border border-white/10 px-5 py-3 font-bold hover:bg-white/10"
            >
              Suivre import
            </Link>
          </div>
        </div>

        <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-2xl font-bold">Prix détaillé</h2>

          <PriceRow label="Prix voiture" value={order.car_price} />
          <PriceRow label="Frais import" value={order.import_fees} />
          <PriceRow label="Frais livraison" value={order.delivery_fees} />

          <div className="mt-6 border-t border-white/10 pt-6">
            <div className="flex justify-between text-2xl font-black">
              <span>Total</span>
              <span>{Number(order.total_price || 0).toLocaleString()} $</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Info({ icon, label, value }) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-2xl bg-black p-4">
      <span className="flex items-center gap-2 text-gray-400">
        {icon}
        {label}
      </span>

      <span className="font-bold">{value}</span>
    </div>
  );
}

function PriceRow({ label, value }) {
  return (
    <div className="mt-5 flex justify-between text-gray-300">
      <span>{label}</span>
      <span className="font-bold">
        {Number(value || 0).toLocaleString()} $
      </span>
    </div>
  );
}