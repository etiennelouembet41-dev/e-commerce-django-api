import { Link } from "react-router-dom";

export default function PaymentCancel() {
  return (
    <section className="mx-auto flex min-h-[80vh] max-w-2xl items-center px-6">
      <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-8">
        <h1 className="text-4xl font-black text-red-400">
          Paiement annulé
        </h1>
        <p className="mt-4 text-gray-300">
          Le paiement n’a pas été finalisé. Vous pouvez réessayer depuis votre commande.
        </p>
        <Link
          to="/cars"
          className="mt-6 inline-block rounded-2xl bg-red-600 px-6 py-3 font-bold"
        >
          Retour au catalogue
        </Link>
      </div>
    </section>
  );
}