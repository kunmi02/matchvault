"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken } from "@/lib/api";

export default function NavBar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    setIsLoggedIn(!!getToken());
  }, [pathname]);

  function handleLogout() {
    clearToken();
    setIsLoggedIn(false);
    router.push("/login");
  }

  const linkClass = "hover:text-emerald-400 transition";

  return (
    <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <a href="/" className="text-xl font-bold text-emerald-400">
          MatchVault
        </a>
        <div className="flex gap-4 text-sm items-center">
          <a href="/dashboard" className={linkClass}>
            Dashboard
          </a>
          <a href="/pots/create" className={linkClass}>
            Create Pot
          </a>
          {isLoggedIn ? (
            <button
              type="button"
              onClick={handleLogout}
              className={`${linkClass} bg-transparent border-none p-0 cursor-pointer text-sm text-slate-100`}
            >
              Logout
            </button>
          ) : (
            <a href="/login" className={linkClass}>
              Login
            </a>
          )}
        </div>
      </div>
    </nav>
  );
}
