import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <section className="mx-auto flex min-h-[80vh] max-w-3xl flex-col items-center justify-center px-6 text-center">
      <p className="text-8xl font-black text-red-600">404</p>

      <h1 className="mt-6 text-4xl font-black">
        Page introuvable
      </h1>

      <p className="mt-4 text-gray-400">
        La page que vous cherchez n’existe pas ou a été déplacée.
      </p>

      <Link
        to="/"
        className="mt-8 rounded-2xl bg-red-600 px-6 py-3 font-black hover:bg-red-700"
      >
        Retour à l’accueil
      </Link>
    </section>
  );
}