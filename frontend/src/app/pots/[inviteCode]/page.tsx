"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, Participant, PotDetails, VirtualAccount } from "@/lib/api";

export default function PotPage() {
  const { inviteCode } = useParams<{ inviteCode: string }>();
  const [pot, setPot] = useState<PotDetails | null>(null);
  const [prediction, setPrediction] = useState("home");
  const [participant, setParticipant] = useState<Participant | null>(null);
  const [va, setVa] = useState<VirtualAccount | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (inviteCode) {
      api.getPotByInvite(inviteCode).then(setPot).catch((e) => setError(e.message));
    }
  }, [inviteCode]);

  async function handleJoin() {
    setLoading(true);
    setError("");
    try {
      const p = await api.joinPot(inviteCode, prediction);
      setParticipant(p);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Join failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateVA() {
    if (!participant) return;
    setLoading(true);
    try {
      const account = await api.generateVA(participant.id);
      setVa(account);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate account");
    } finally {
      setLoading(false);
    }
  }

  if (!pot) {
    return <p className="text-slate-400">{error || "Loading pot..."}</p>;
  }

  const predictions =
    pot.prediction_type === "winner"
      ? [
          { value: "home", label: pot.match?.home_team || "Home" },
          { value: "draw", label: "Draw" },
          { value: "away", label: pot.match?.away_team || "Away" },
        ]
      : [
          { value: "over", label: "Over 2.5" },
          { value: "under", label: "Under 2.5" },
        ];

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{pot.name}</h1>
        <p className="text-slate-400 mt-1">
          {pot.match
            ? `${pot.match.home_team} vs ${pot.match.away_team}`
            : "Match TBD"}{" "}
          · ₦{pot.stake_amount.toLocaleString()} stake
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
        <p className="text-sm text-slate-400">Invite link</p>
        <code className="text-emerald-400 text-sm break-all">{pot.invite_link}</code>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="font-medium mb-3">
          Participants ({pot.participants.length})
        </p>
        {pot.participants.length === 0 ? (
          <p className="text-slate-400 text-sm">No participants yet</p>
        ) : (
          <ul className="space-y-2">
            {pot.participants.map((p) => (
              <li key={p.id} className="flex justify-between text-sm">
                <span>{p.prediction}</span>
                <span
                  className={
                    p.status === "paid" ? "text-emerald-400" : "text-slate-400"
                  }
                >
                  {p.status}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {!participant && pot.status === "open" && (
        <div className="space-y-4">
          <h2 className="font-semibold">Join this pot</h2>
          <div className="flex gap-2 flex-wrap">
            {predictions.map((p) => (
              <button
                key={p.value}
                onClick={() => setPrediction(p.value)}
                className={`px-4 py-2 rounded-lg text-sm border transition ${
                  prediction === p.value
                    ? "border-emerald-500 bg-emerald-500/10 text-emerald-400"
                    : "border-slate-700 hover:border-slate-500"
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
          <button
            onClick={handleJoin}
            disabled={loading}
            className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold py-3 rounded-lg disabled:opacity-50"
          >
            {loading ? "Joining..." : "Join Pot"}
          </button>
        </div>
      )}

      {participant && !va && (
        <button
          onClick={handleGenerateVA}
          disabled={loading}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold py-3 rounded-lg disabled:opacity-50"
        >
          {loading ? "Generating..." : "Get Payment Account"}
        </button>
      )}

      {va && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-6 space-y-3">
          <h2 className="font-semibold text-emerald-400">Pay ₦{va.amount.toLocaleString()}</h2>
          <p className="text-sm text-slate-300">
            Transfer to this Virtual Account:
          </p>
          <p className="text-2xl font-mono font-bold">{va.virtual_account_number}</p>
          <p className="text-xs text-slate-400">Ref: {va.virtual_account_reference}</p>
        </div>
      )}

      {error && <p className="text-red-400 text-sm">{error}</p>}
    </div>
  );
}
