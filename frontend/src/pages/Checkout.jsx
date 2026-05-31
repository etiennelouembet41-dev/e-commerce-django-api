import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

export default function Checkout() {
  const { carId } = useParams();

  const [car, setCar] = useState(null);
  const [cities, setCities] = useState([]);
  const [addresses, setAddresses] = useState([]);

  const [deliveryCity, setDeliveryCity] = useState("");
  const [deliveryAddress, setDeliveryAddress] = useState("");
  const [paymentType, setPaymentType] = useState("deposit");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/cars/${carId}/`).then((res) => setCar(res.data));
    api.get("/cities/").then((res) => setCities(res.data.results || res.data));
    api.get("/addresses/").then((res) => setAddresses(res.data.results || res.data));
  }, [carId]);

  const handleCheckout = async () => {
    setLoading(true);
    setError("");

    try {
      const orderRes = await api.post("/orders/", {
        car: carId,
        delivery_city: deliveryCity,
        delivery_address: deliveryAddress,
        status: "pending",
      });

      const paymentRes = await api.post("/payments/create-checkout-session/", {
        order_id: orderRes.data.id,
        payment_type: paymentType,
      });

      window.location.href = paymentRes.data.checkout_url;
    } catch {
      setError("Impossible de créer la commande ou le paiement.");
    } finally {
      setLoading(false);
    }
  };

  if (!car) return <div className="p-6 text-gray-400">Chargement...</div>;

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-4xl font-black">Checkout</h1>

      {error && (
        <div className="mt-6 rounded-xl bg-red-500/10 p-4 text-red-400">
          {error}
        </div>
      )}

      <div className="mt-8 grid gap-8 lg:grid-cols-2">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-2xl font-bold">
            {car.brand} {car.model}
          </h2>

          <p className="mt-2 text-gray-400">Prix voiture</p>
          <p className="text-3xl font-black">
            {Number(car.price).toLocaleString()} MYR
          </p>

          <div className="mt-6">
            <label className="text-sm text-gray-400">Ville de livraison</label>
            <select
              value={deliveryCity}
              onChange={(e) => setDeliveryCity(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
            >
              <option value="">Choisir une ville</option>
              {cities.map((city) => (
                <option key={city.id} value={city.id}>
                  {city.name} - {city.delivery_price} MYR
                </option>
              ))}
            </select>
          </div>

          <div className="mt-5">
            <label className="text-sm text-gray-400">Adresse</label>
            <select
              value={deliveryAddress}
              onChange={(e) => setDeliveryAddress(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
            >
              <option value="">Choisir une adresse</option>
              {addresses.map((address) => (
                <option key={address.id} value={address.id}>
                  {address.address_line}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-5">
            <label className="text-sm text-gray-400">Paiement</label>
            <select
              value={paymentType}
              onChange={(e) => setPaymentType(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
            >
              <option value="deposit">Acompte 20%</option>
              <option value="full">Paiement total</option>
            </select>
          </div>

          <button
            onClick={handleCheckout}
            disabled={loading || !deliveryCity || !deliveryAddress}
            className="mt-8 w-full rounded-2xl bg-red-600 py-4 font-black hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? "Redirection Stripe..." : "Payer avec Stripe"}
          </button>
        </div>
      </div>
    </section>
  );
}