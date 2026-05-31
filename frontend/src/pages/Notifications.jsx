import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);

  const fetchNotifications = async () => {
    const res = await api.get("/notifications/");
    setNotifications(res.data.results || res.data);
  };

  const markAsRead = async (id) => {
    await api.post(`/notifications/${id}/mark-as-read/`);

    setNotifications((prev) =>
      prev.map((n) =>
        n.id === id ? { ...n, is_read: true } : n
      )
    );
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-4xl font-black">
        Notifications
      </h1>

      <div className="mt-8 space-y-4">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={`rounded-3xl border p-5 ${
              notification.is_read
                ? "border-white/10 bg-white/5"
                : "border-red-500/30 bg-red-500/10"
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold">
                  {notification.title}
                </h3>

                <p className="mt-2 text-gray-400">
                  {notification.message}
                </p>
              </div>

              {!notification.is_read && (
                <button
                  onClick={() =>
                    markAsRead(notification.id)
                  }
                  className="rounded-xl bg-red-600 px-4 py-2"
                >
                  Lu
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}