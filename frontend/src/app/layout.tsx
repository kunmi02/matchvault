import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MatchVault",
  description: "Seamless group match pots with instant payments and automatic settlements",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-950 text-slate-100 min-h-screen`}>
        <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
          <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
            <a href="/" className="text-xl font-bold text-emerald-400">
              MatchVault
            </a>
            <div className="flex gap-4 text-sm">
              <a href="/dashboard" className="hover:text-emerald-400 transition">
                Dashboard
              </a>
              <a href="/pots/create" className="hover:text-emerald-400 transition">
                Create Pot
              </a>
              <a href="/login" className="hover:text-emerald-400 transition">
                Login
              </a>
            </div>
          </div>
        </nav>
        <main className="max-w-5xl mx-auto px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
