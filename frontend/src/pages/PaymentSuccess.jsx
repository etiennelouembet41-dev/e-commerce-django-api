import { Link } from "react-router-dom";

export default function PaymentSuccess() {
  return (
    <section className="mx-auto flex min-h-[80vh] max-w-2xl items-center px-6">
      <div className="rounded-3xl border border-green-500/20 bg-green-500/10 p-8">
        <h1 className="text-4xl font-black text-green-400">
          Paiement confirmé
        </h1>
        <p className="mt-4 text-gray-300">
          Votre paiement a été reçu. La voiture est maintenant réservée.
        </p>
        <Link
          to="/tracking"
          className="mt-6 inline-block rounded-2xl bg-red-600 px-6 py-3 font-bold"
        >
          Suivre ma commande
        </Link>
      </div>
    </section>
  );
}