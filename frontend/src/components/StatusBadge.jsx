export default function StatusBadge({ value }) {
  const colors = {
    unpaid: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    deposit_paid: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    paid: "bg-green-500/10 text-green-400 border-green-500/20",
    failed: "bg-red-500/10 text-red-400 border-red-500/20",
    refunded: "bg-purple-500/10 text-purple-400 border-purple-500/20",

    pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    confirmed: "bg-green-500/10 text-green-400 border-green-500/20",
    processing: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    importing: "bg-orange-500/10 text-orange-400 border-orange-500/20",
    delivering: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    completed: "bg-green-500/10 text-green-400 border-green-500/20",
    cancelled: "bg-red-500/10 text-red-400 border-red-500/20",

    supplier_purchase: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    documents_preparation: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    international_shipping: "bg-orange-500/10 text-orange-400 border-orange-500/20",
    malaysia_customs: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    local_delivery: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    delivered: "bg-green-500/10 text-green-400 border-green-500/20",
  };

  return (
    <span
      className={`rounded-full border px-3 py-1 text-sm font-bold ${
        colors[value] || "border-white/10 bg-white/5 text-gray-300"
      }`}
    >
      {value}
    </span>
  );
}
