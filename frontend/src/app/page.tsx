import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="text-center space-y-6 pt-12">
        <p className="text-emerald-400 font-medium tracking-wide uppercase text-sm">
          FIFA World Cup 2026
        </p>
        <h1 className="text-5xl font-bold leading-tight">
          Group match pots with{" "}
          <span className="text-emerald-400">instant payments</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Create prediction pots, collect stakes via Nomba Virtual Accounts, and
          settle winners automatically — no manual chasing or disputes.
        </p>
        <div className="flex gap-4 justify-center pt-4">
          <Link
            href="/pots/create"
            className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-6 py-3 rounded-lg transition"
          >
            Create a Pot
          </Link>
          <Link
            href="/dashboard"
            className="border border-slate-700 hover:border-emerald-500 px-6 py-3 rounded-lg transition"
          >
            View Dashboard
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        {[
          {
            title: "Create & Invite",
            desc: "Pick a match, set stake and rules, share your invite link.",
          },
          {
            title: "Pay via Nomba",
            desc: "Each participant gets a dynamic Virtual Account + QR for instant payment.",
          },
          {
            title: "Auto Settle",
            desc: "Winners calculated from live results, payouts via Bank Transfer API.",
          },
        ].map((f) => (
          <div
            key={f.title}
            className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-2"
          >
            <h3 className="font-semibold text-emerald-400">{f.title}</h3>
            <p className="text-slate-400 text-sm">{f.desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
