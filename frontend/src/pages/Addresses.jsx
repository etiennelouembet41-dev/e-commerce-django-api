import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Addresses() {
  const [addresses, setAddresses] = useState([]);
  const [cities, setCities] = useState([]);

  const [form, setForm] = useState({
    city: "",
    address_line: "",
    postal_code: "",
    is_default: false,
  });

  const fetchData = async () => {
    const addressRes = await api.get("/addresses/");
    const cityRes = await api.get("/cities/");

    setAddresses(addressRes.data.results || addressRes.data);
    setCities(cityRes.data.results || cityRes.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const createAddress = async (e) => {
    e.preventDefault();

    await api.post("/addresses/", form);

    setForm({
      city: "",
      address_line: "",
      postal_code: "",
      is_default: false,
    });

    fetchData();
  };

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-4xl font-black">Mes adresses</h1>

      <form
        onSubmit={createAddress}
        className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-6"
      >
        <h2 className="text-2xl font-bold">Ajouter une adresse</h2>

        <select
          value={form.city}
          onChange={(e) => setForm({ ...form, city: e.target.value })}
          className="mt-5 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
          required
        >
          <option value="">Choisir une ville</option>
          {cities.map((city) => (
            <option key={city.id} value={city.id}>
              {city.name}
            </option>
          ))}
        </select>

        <textarea
          value={form.address_line}
          onChange={(e) =>
            setForm({ ...form, address_line: e.target.value })
          }
          placeholder="Adresse complète"
          className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
          required
        />

        <input
          value={form.postal_code}
          onChange={(e) =>
            setForm({ ...form, postal_code: e.target.value })
          }
          placeholder="Code postal"
          className="mt-4 w-full rounded-2xl border border-white/10 bg-black px-4 py-3"
        />

        <label className="mt-4 flex items-center gap-3 text-gray-300">
          <input
            type="checkbox"
            checked={form.is_default}
            onChange={(e) =>
              setForm({ ...form, is_default: e.target.checked })
            }
          />
          Adresse par défaut
        </label>

        <button className="mt-6 rounded-2xl bg-red-600 px-6 py-3 font-black hover:bg-red-700">
          Ajouter
        </button>
      </form>

      <div className="mt-10 grid gap-4">
        {addresses.map((address) => (
          <div
            key={address.id}
            className="rounded-3xl border border-white/10 bg-white/5 p-5"
          >
            <p className="font-bold">{address.address_line}</p>
            <p className="mt-2 text-gray-400">
              Code postal : {address.postal_code || "Non défini"}
            </p>
            {address.is_default && (
              <span className="mt-3 inline-block rounded-full bg-red-600 px-3 py-1 text-sm">
                Par défaut
              </span>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}