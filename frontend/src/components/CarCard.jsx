import { Link } from "react-router-dom";
import { Gauge, MapPin, Zap } from "lucide-react";
import { motion } from "framer-motion";

export default function CarCard({ car }) {
  return (
    <motion.div initial={{ opacity: 0, y: 25 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
      <Link
        to={`/cars/${car.id}`}
        className="group block overflow-hidden rounded-3xl border border-white/10 bg-white/5 shadow-xl transition hover:-translate-y-1 hover:bg-white/10"
      >

      <div className="h-56 overflow-hidden bg-neutral-900">
        {car.main_image ? (
          <img
            src={car.main_image}
            alt={`${car.brand} ${car.model}`}
            className="h-full w-full object-cover transition duration-500 group-hover:scale-110"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-500">
            Aucune image
          </div>
        )}
      </div>

      <div className="p-5">
        <p className="text-sm uppercase text-red-500">{car.race_type}</p>

        <h3 className="mt-1 text-xl font-bold">
          {car.brand} {car.model}
        </h3>

        <p className="mt-2 text-2xl font-black text-white">
          {Number(car.price).toLocaleString()} MYR
        </p>

        <div className="mt-4 grid grid-cols-3 gap-3 text-sm text-gray-400">
          <span className="flex items-center gap-1">
            <Zap size={16} /> {car.power_hp} HP
          </span>
          <span className="flex items-center gap-1">
            <Gauge size={16} /> {car.mileage} km
          </span>
          <span className="flex items-center gap-1">
            <MapPin size={16} /> #{car.origin_country_name}
          </span>
        </div>
      </div>
    </Link>
  </motion.div>
  );
}