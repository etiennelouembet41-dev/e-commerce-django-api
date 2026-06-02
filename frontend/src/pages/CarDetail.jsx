import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Gauge, Zap, Fuel, Settings, MapPin } from "lucide-react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function CarDetail() {
  const { id } = useParams();
  const [car, setCar] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchCar = async () => {
    try {
      const res = await api.get(`/cars/${id}/`);
      setCar(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCar();
  }, [id]);

  if (loading) return <div className="p-6 text-gray-400">Chargement...</div>;
  if (!car) return <div className="p-6 text-gray-400">Voiture introuvable.</div>;

  return (
    <section className="mx-auto max-w-7xl px-6 py-12">
      <div className="grid gap-10 lg:grid-cols-2">
        <div>
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
            {car.main_image ? (
              <img
                src={car.main_image}
                alt={`${car.brand} ${car.model}`}
                className="h-[520px] w-full object-cover"
              />
            ) : (
              <div className="flex h-[520px] items-center justify-center text-gray-500">
                Aucune image
              </div>
            )}
          </div>

          {car.gallery?.length > 0 && (
            <div className="mt-4 grid grid-cols-4 gap-3">
              {car.gallery.map((img) => (
                <img
                  key={img.id}
                  src={img.image}
                  alt=""
                  className="h-24 rounded-2xl object-cover"
                />
              ))}
            </div>
          )}
        </div>

        <div>
          <p className="text-sm font-bold uppercase text-red-500">
            {car.race_type}
          </p>

          <h1 className="mt-2 text-5xl font-black">
            {car.brand} {car.model}
          </h1>

          <p className="mt-3 text-gray-400">Année {car.year}</p>

          <div className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-6">
            <p className="text-gray-400">Prix voiture</p>
            <p className="mt-1 text-4xl font-black">
              {Number(car.price).toLocaleString()} MYR
            </p>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-4">
            <Info icon={<Zap />} label="Puissance" value={`${car.power_hp} HP`} />
            <Info icon={<Gauge />} label="Kilométrage" value={`${car.mileage} km`} />
            <Info icon={<Settings />} label="Transmission" value={car.transmission} />
            <Info icon={<Fuel />} label="Carburant" value={car.fuel} />
            <Info icon={<MapPin />} label="Pays origine" value={`${car.origin_country_name}`} />
            <Info label="État" value={car.conditions} />
          </div>

          <div className="mt-8">
            <h2 className="text-2xl font-bold">Description</h2>
            <p className="mt-3 leading-8 text-gray-300">{car.description}</p>
          </div>

          <button
            onClick={() => navigate(`/checkout/${car.id}`)}
            className="mt-8 w-full rounded-2xl bg-red-600 py-4 text-lg font-black hover:bg-red-700"
          >
            Commander cette voiture
          </button>

        </div>
      </div>
    </section>
  );
}

function Info({ icon, label, value }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="flex items-center gap-2 text-red-500">
        {icon}
        <span className="text-sm font-semibold">{label}</span>
      </div>
      <p className="mt-2 font-bold">{value}</p>
    </div>
  );
}