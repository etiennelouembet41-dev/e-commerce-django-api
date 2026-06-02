import { Link } from "react-router-dom";
import { Car, Mail, Phone, MapPin,} from "lucide-react";
import logo from "../assets/logo.png";

export default function Footer() {
  return (
    <footer className="mt-20 border-t border-white/10 bg-black">
      <div className="mx-auto max-w-7xl px-6 py-14">
        <div className="grid gap-10 md:grid-cols-4">
          <div>
            <div className="flex items-center gap-2">
              <img src={logo} alt="Le Vikings Cars" className="h-10 w-auto"/>
              <span className="text-xl font-black">
                Le_Vikings_Cars
              </span>
            </div>

            <p className="mt-4 text-gray-400">
              Importation de voitures de course
              d’occasion en Malaisie.
            </p>
          </div>

          <div>
            <h3 className="font-bold">Navigation</h3>

            <div className="mt-4 flex flex-col gap-2 text-gray-400">
              <Link to="/">Accueil</Link>
              <Link to="/cars">Catalogue</Link>
              <Link to="/assistant">Assistant IA</Link>
              <Link to="/orders">Commandes</Link>
            </div>
          </div>

          <div>
            <h3 className="font-bold">Compte</h3>

            <div className="mt-4 flex flex-col gap-2 text-gray-400">
              <Link to="/profile">Profil</Link>
              <Link to="/addresses">Adresses</Link>
              <Link to="/notifications">Notifications</Link>
              <Link to="/tracking">Suivi import</Link>
            </div>
          </div>

          <div>
            <h3 className="font-bold">Contact</h3>

            <div className="mt-4 space-y-3 text-gray-400">
              <p className="flex items-center gap-2">
                <Mail size={18} />
                contact@levikingscars.com
              </p>

              <p className="flex items-center gap-2">
                <Phone size={18} />
                +60 12 345 6789
              </p>

              <p className="flex items-center gap-2">
                <MapPin size={18} />
                Kuala Lumpur, Malaysia
              </p>
            </div>
          </div>
        </div>

        <div className="mt-10 border-t border-white/10 pt-6 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} Le_Vikings_Cars.
          Tous droits réservés.
        </div>
      </div>
    </footer>
  );
}