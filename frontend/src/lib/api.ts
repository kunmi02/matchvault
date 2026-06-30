const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function setToken(token: string) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  register: (email: string, password: string, name?: string) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getUpcomingMatches: () => request<Match[]>("/matches/upcoming"),

  createPot: (data: CreatePotInput) =>
    request<Pot>("/pots", { method: "POST", body: JSON.stringify(data) }),

  getMyPots: () => request<Pot[]>("/pots/my"),

  getPotByInvite: (inviteCode: string) => request<PotDetails>(`/pots/${inviteCode}`),

  joinPot: (inviteCode: string, prediction: string) =>
    request<Participant>(`/pots/${inviteCode}/join`, {
      method: "POST",
      body: JSON.stringify({ prediction }),
    }),

  generateVA: (participantId: string) =>
    request<VirtualAccount>(`/pots/${participantId}/generate-va`, { method: "POST" }),

  getDashboard: () => request<Dashboard>("/dashboard"),

  settlePot: (potId: string) =>
    request(`/pots/${potId}/settle`, { method: "POST" }),
};

export interface Match {
  id: number;
  home_team: string;
  away_team: string;
  match_date: string;
  status: string;
}

export interface Pot {
  id: string;
  name: string;
  description?: string;
  stake_amount: number;
  prediction_type: string;
  status: string;
  invite_code: string;
  invite_link?: string;
  participant_count: number;
  match?: Match;
}

export interface Participant {
  id: string;
  prediction: string;
  status: string;
  paid_amount: number;
  virtual_account_number?: string;
}

export interface PotDetails extends Pot {
  participants: Participant[];
}

export interface VirtualAccount {
  participant_id: string;
  virtual_account_number: string;
  virtual_account_reference: string;
  amount: number;
}

export interface Dashboard {
  pots_created: number;
  pots_joined: number;
  total_staked: number;
  open_pots: number;
  recent_pots: Pot[];
}

export interface CreatePotInput {
  match_id: number;
  name: string;
  description?: string;
  stake_amount: number;
  prediction_type: "winner" | "over_under";
  max_participants?: number;
  creator_fee_percent?: number;
}
