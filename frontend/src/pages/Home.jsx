import { Link } from "react-router-dom";
import { Bot, CreditCard, Globe2, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <section>
      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }} className="mx-auto grid min-h-[85vh] max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-2">
        <div>
          <p className="text-sm font-bold uppercase text-red-500">
            Race cars import platform
          </p>

          <h1 className="mt-4 text-5xl font-black leading-tight md:text-7xl">
            Importez votre voiture de course d’occasion.
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-400">
            Découvrez des voitures préparées pour circuit, drift, rallye et drag race.
            Paiement sécurisé, suivi logistique et assistant IA Gemini.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/cars"
              className="rounded-2xl bg-red-600 px-7 py-4 font-black hover:bg-red-700"
            >
              Voir le catalogue
            </Link>

            <Link
              to="/assistant"
              className="rounded-2xl border border-white/10 px-7 py-4 font-black hover:bg-white/10"
            >
              Demander à l’IA
            </Link>
          </div>
        </div>

        <div className="rounded-[2rem] border border-white/10 bg-white/5 p-4 shadow-2xl">
          <div className="rounded-[1.5rem] bg-gradient-to-br from-red-600/30 to-black p-8">
            <h2 className="text-3xl font-black">Nissan Skyline GT-R R34</h2>
            <p className="mt-3 text-gray-300">Circuit • 500 HP • Japon</p>
            <p className="mt-8 text-5xl font-black">450,000 MYR</p>
          </div>
        </div>
      </motion.div>

      <div className="mx-auto grid max-w-7xl gap-5 px-6 pb-20 md:grid-cols-4">
        <Feature icon={<Globe2 />} title="Import international" />
        <Feature icon={<CreditCard />} title="Paiement Stripe sécurisé" />
        <Feature icon={<Bot />} title="Conseil IA Gemini" />
        <Feature icon={<ShieldCheck />} title="Suivi logistique complet" />
      </div>
    </section>
  );
}

function Feature({ icon, title }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
      <div className="text-red-500">{icon}</div>
      <h3 className="mt-4 font-bold">{title}</h3>
    </div>
  );
}