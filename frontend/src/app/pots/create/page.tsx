"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, CreatePotInput, Match } from "@/lib/api";

function Field({
  label,
  hint,
  children,
}: {
  label: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-200">{label}</label>
      {hint && <p className="text-xs text-slate-500 mt-0.5 mb-2">{hint}</p>}
      {!hint && <div className="mb-2" />}
      {children}
    </div>
  );
}

const inputClass =
  "w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder:text-slate-600";

function parseWholeNumber(value: string): number {
  const digits = value.replace(/\D/g, "");
  if (!digits) return 0;
  return parseInt(digits, 10);
}

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
    if (form.stake_amount < 100) {
      setError("Stake must be at least ₦100");
      return;
    }
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

  function formatMatchDate(date: string) {
    return new Date(date).toLocaleString(undefined, {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  }

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Create a Pot</h1>
        <p className="text-slate-400 text-sm mt-1">
          Set up a group pool for a match. Share the invite link so friends can join and pay
          their stake.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <Field
          label="Match"
          hint="Choose the fixture everyone will predict on."
        >
          <select
            value={form.match_id}
            onChange={(e) => setForm({ ...form, match_id: Number(e.target.value) })}
            className={inputClass}
            required
          >
            <option value={0}>Select a match</option>
            {matches.map((m) => (
              <option key={m.id} value={m.id}>
                {m.home_team} vs {m.away_team}
                {m.match_date ? ` — ${formatMatchDate(m.match_date)}` : ""}
              </option>
            ))}
          </select>
        </Field>

        <Field
          label="Pot name"
          hint="Something your group will recognize, e.g. “Office WC Final” or “Lagos crew”."
        >
          <input
            placeholder="e.g. Nigeria vs Argentina — office pool"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className={inputClass}
            required
          />
        </Field>

        <Field
          label="Stake per person (₦)"
          hint="How much each participant must pay to join. Minimum ₦100."
        >
          <input
            type="text"
            inputMode="numeric"
            placeholder="1000"
            value={form.stake_amount || ""}
            onChange={(e) =>
              setForm({ ...form, stake_amount: parseWholeNumber(e.target.value) })
            }
            className={inputClass}
            required
          />
        </Field>

        <Field
          label="What are people predicting?"
          hint={
            form.prediction_type === "winner"
              ? "Each person picks home win, draw, or away win. Everyone who picks correctly shares the prize pool."
              : "Each person picks over or under 2.5 total goals. Correct picks share the prize pool."
          }
        >
          <select
            value={form.prediction_type}
            onChange={(e) =>
              setForm({ ...form, prediction_type: e.target.value as "winner" | "over_under" })
            }
            className={inputClass}
          >
            <option value="winner">Match result (home / draw / away)</option>
            <option value="over_under">Total goals (over / under 2.5)</option>
          </select>
        </Field>

        <Field
          label="Your organizer fee (%)"
          hint="Optional cut you take from the total pool before winnings are paid out. Set to 0 for no fee."
        >
          <input
            type="text"
            inputMode="numeric"
            placeholder="0"
            value={String(form.creator_fee_percent)}
            onChange={(e) =>
              setForm({
                ...form,
                creator_fee_percent: Math.min(parseWholeNumber(e.target.value), 100),
              })
            }
            className={inputClass}
          />
        </Field>

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
