import { useEffect, useState } from "react";
import {
  Car,
  CreditCard,
  Package,
  TrendingUp,
  Bot,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import api from "../api/axios";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/dashboard/stats/").then((res) => setStats(res.data));
  }, []);

  if (!stats) {
    return <div className="p-6 text-gray-400">Chargement dashboard...</div>;
  }

  const monthlySales = stats.monthly_sales || [];
  const salesByCity = stats.sales_by_city || [];
  const salesByRaceType = stats.sales_by_race_type || [];

  return (
    <section className="mx-auto max-w-7xl px-6 py-12">
      <p className="text-sm font-bold uppercase text-red-500">
        Administration
      </p>

      <h1 className="mt-2 text-4xl font-black">
        Dashboard Le_Vikings_Cars
      </h1>

      <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={<TrendingUp />}
          label="Chiffre d’affaires"
          value={`${Number(stats.total_revenue?.total || 0).toLocaleString()} MYR`}
        />

        <StatCard
          icon={<Package />}
          label="Commandes"
          value={stats.total_orders}
        />

        <StatCard
          icon={<Car />}
          label="Voitures disponibles"
          value={stats.available_cars}
        />

        <StatCard
          icon={<CreditCard />}
          label="Paiements reçus"
          value={`${Number(stats.payments_received?.total || 0).toLocaleString()} MYR`}
        />
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ChartCard title="Ventes mensuelles">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={monthlySales}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Ventes par type de course">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={salesByRaceType}>
              <XAxis dataKey="car__race_type" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_orders" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ListCard
          title="Ventes par ville"
          items={salesByCity}
          labelKey="delivery_city__name"
          valueKey="total"
        />

        <ListCard
          title="Top voitures vendues"
          items={stats.top_selling_cars || []}
          customLabel={(item) => `${item.car__brand} ${item.car__model}`}
          valueKey="total_orders"
        />
      </div>

      <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-6">
        <div className="flex items-center gap-3">
          <Bot className="text-red-500" />
          <h2 className="text-2xl font-bold">Statistiques IA</h2>
        </div>

        <p className="mt-4 text-gray-400">
          Questions IA totales :{" "}
          <span className="font-bold text-white">
            {stats.total_ai_questions || 0}
          </span>
        </p>

        <div className="mt-6 space-y-3">
          {(stats.frequent_ai_questions || []).map((q, index) => (
            <div
              key={index}
              className="rounded-2xl border border-white/10 bg-black p-4"
            >
              <p>{q.question}</p>
              <p className="mt-1 text-sm text-gray-500">
                Total : {q.total}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
      <div className="text-red-500">{icon}</div>
      <p className="mt-4 text-gray-400">{label}</p>
      <p className="mt-2 text-3xl font-black">{value}</p>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
      <h2 className="mb-6 text-xl font-bold">{title}</h2>
      {children}
    </div>
  );
}

function ListCard({ title, items, labelKey, valueKey, customLabel }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
      <h2 className="mb-6 text-xl font-bold">{title}</h2>

      <div className="space-y-3">
        {items.map((item, index) => (
          <div
            key={index}
            className="flex justify-between rounded-2xl bg-black p-4"
          >
            <span>
              {customLabel ? customLabel(item) : item[labelKey]}
            </span>
            <span className="font-bold text-red-500">
              {item[valueKey]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}