import { useState } from "react";
import { Bot, Send, User } from "lucide-react";
import api from "../api/axios";

export default function Assistant() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Bonjour, je peux vous aider à choisir une voiture de course d’occasion selon votre budget, usage et import en Malaisie.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setInput("");
    setLoading(true);

    try {
      const res = await api.post("/ai/chat/", {
        message: userMessage,
      });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.data.reply },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Une erreur est survenue avec l’assistant IA.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto flex min-h-[85vh] max-w-4xl flex-col px-6 py-10">
      <div className="mb-6">
        <p className="text-sm font-bold uppercase text-red-500">
          Assistant IA Gemini
        </p>
        <h1 className="mt-2 text-4xl font-black">
          Trouvez la voiture idéale
        </h1>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto rounded-3xl border border-white/10 bg-white/5 p-6">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.role === "assistant" && (
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-600">
                <Bot size={20} />
              </div>
            )}

            <div
              className={`max-w-[75%] rounded-3xl px-5 py-4 leading-7 ${
                msg.role === "user"
                  ? "bg-red-600 text-white"
                  : "bg-black text-gray-200"
              }`}
            >
              {msg.content}
            </div>

            {msg.role === "user" && (
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10">
                <User size={20} />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <p className="text-sm text-gray-400">Gemini réfléchit...</p>
        )}
      </div>

      <form onSubmit={sendMessage} className="mt-5 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ex: Je cherche une voiture drift sous 60 000 MYR import inclus..."
          className="flex-1 rounded-2xl border border-white/10 bg-black px-5 py-4 outline-none focus:border-red-500"
        />

        <button className="rounded-2xl bg-red-600 px-6 font-black hover:bg-red-700">
          <Send size={22} />
        </button>
      </form>
    </section>
  );
}