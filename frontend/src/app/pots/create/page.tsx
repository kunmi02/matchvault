"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, CreatePotInput, Match } from "@/lib/api";

export default function CreatePotPage() {
  const router = useRouter();
  const [matches, setMatches] = useState<Match[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<CreatePotInput>({
    match_id: 0,
    name: "",
    stake_amount: 1000,
    prediction_type: "winner",
    creator_fee_percent: 5,
  });

  useEffect(() => {
    api.getUpcomingMatches().then(setMatches).catch(() => setError("Login required"));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const pot = await api.createPot(form);
      router.push(`/pots/${pot.invite_code}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create pot");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Create a Pot</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="text-sm text-slate-400">Match</label>
          <select
            value={form.match_id}
            onChange={(e) => setForm({ ...form, match_id: Number(e.target.value) })}
            className="w-full mt-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3"
            required
          >
            <option value={0}>Select a match</option>
            {matches.map((m) => (
              <option key={m.id} value={m.id}>
                {m.home_team} vs {m.away_team}
              </option>
            ))}
          </select>
        </div>
        <input
          placeholder="Pot name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3"
          required
        />
        <input
          type="number"
          placeholder="Stake amount (₦)"
          value={form.stake_amount}
          onChange={(e) => setForm({ ...form, stake_amount: Number(e.target.value) })}
          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3"
          min={100}
          required
        />
        <div>
          <label className="text-sm text-slate-400">Prediction type</label>
          <select
            value={form.prediction_type}
            onChange={(e) =>
              setForm({ ...form, prediction_type: e.target.value as "winner" | "over_under" })
            }
            className="w-full mt-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3"
          >
            <option value="winner">Match Winner</option>
            <option value="over_under">Over / Under Goals</option>
          </select>
        </div>
        <input
          type="number"
          placeholder="Creator fee %"
          value={form.creator_fee_percent}
          onChange={(e) =>
            setForm({ ...form, creator_fee_percent: Number(e.target.value) })
          }
          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3"
          min={0}
          max={100}
        />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold py-3 rounded-lg disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create Pot & Get Invite Link"}
        </button>
      </form>
    </div>
  );
}
