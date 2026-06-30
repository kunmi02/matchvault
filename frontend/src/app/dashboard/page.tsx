"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, Dashboard, Pot } from "@/lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [pots, setPots] = useState<Pot[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.getDashboard(), api.getMyPots()])
      .then(([dash, myPots]) => {
        setData(dash);
        setPots(myPots);
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="text-center space-y-4">
        <p className="text-red-400">{error}</p>
        <Link href="/login" className="text-emerald-400 hover:underline">
          Login to continue
        </Link>
      </div>
    );
  }

  if (!data) return <p className="text-slate-400">Loading dashboard...</p>;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <Link
          href="/pots/create"
          className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-4 py-2 rounded-lg text-sm"
        >
          + New Pot
        </Link>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Pots Created", value: data.pots_created },
          { label: "Pots Joined", value: data.pots_joined },
          { label: "Total Staked", value: `₦${data.total_staked.toLocaleString()}` },
          { label: "Open Pots", value: data.open_pots },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4"
          >
            <p className="text-slate-400 text-sm">{stat.label}</p>
            <p className="text-2xl font-bold mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">Your Pots</h2>
        {pots.length === 0 ? (
          <p className="text-slate-400">No pots yet. Create one to get started.</p>
        ) : (
          <div className="space-y-3">
            {pots.map((pot) => (
              <div
                key={pot.id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex justify-between items-center"
              >
                <div>
                  <p className="font-medium">{pot.name}</p>
                  <p className="text-slate-400 text-sm">
                    {pot.match
                      ? `${pot.match.home_team} vs ${pot.match.away_team}`
                      : "—"}{" "}
                    · ₦{pot.stake_amount.toLocaleString()} · {pot.participant_count}{" "}
                    joined
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <span
                    className={`text-xs px-2 py-1 rounded-full ${
                      pot.status === "open"
                        ? "bg-emerald-500/20 text-emerald-400"
                        : "bg-slate-700 text-slate-300"
                    }`}
                  >
                    {pot.status}
                  </span>
                  <Link
                    href={`/pots/${pot.invite_code}`}
                    className="text-emerald-400 text-sm hover:underline"
                  >
                    View
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
