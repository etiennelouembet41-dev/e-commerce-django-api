import { useEffect, useState } from "react";
import api from "../api/axios";
import CarCard from "../components/CarCard";

export default function Cars() {
  const [cars, setCars] = useState([]);
  const [search, setSearch] = useState("");
  const [raceType, setRaceType] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchCars = async () => {
    setLoading(true);

    try {
      const params = new URLSearchParams();

      if (search) params.append("search", search);
      if (raceType) params.append("race_type", raceType);

      const res = await api.get(`/cars/?${params.toString()}`);

      setCars(res.data.results || res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCars();
  }, []);

  return (
    <section className="mx-auto max-w-7xl px-6 py-12">
      <div className="mb-10 flex flex-col justify-between gap-6 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-semibold uppercase text-red-500">
            Catalogue
          </p>
          <h1 className="mt-2 text-4xl font-black">
            Voitures de course disponibles
          </h1>
          <p className="mt-3 text-gray-400">
            Filtrez par usage, marque ou modèle.
          </p>
        </div>

        <div className="flex flex-col gap-3 md:flex-row">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher Nissan, Supra..."
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-red-500"
          />

          <select
            value={raceType}
            onChange={(e) => setRaceType(e.target.value)}
            className="rounded-2xl border border-white/10 bg-black text-white px-4 py-3 outline-none focus:border-red-500"
          >
            <option value="" className="bg-black text-white">
              Tous types
            </option>
            <option value="circuit" className="bg-black text-white">
              Circuit
            </option>
            <option value="drift" className="bg-black text-white">
              Drift
            </option>
            <option value="rally" className="bg-black text-white">
              Rallye
            </option>
            <option value="drag" className="bg-black text-white">
              Drag Race
            </option>
            <option value="amateur" className="bg-black text-white">
              Compétition amateur
            </option>
          </select>

          <button
            onClick={fetchCars}
            className="rounded-2xl bg-red-600 px-6 py-3 font-bold hover:bg-red-700"
          >
            Filtrer
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-gray-400">Chargement...</p>
      ) : cars.length === 0 ? (
        <p className="text-gray-400">Aucune voiture trouvée.</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {cars.map((car) => (
            <CarCard key={car.id} car={car} />
          ))}
        </div>
      )}
    </section>
  );
}