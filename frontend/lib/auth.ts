/**
 * TODO (feature/auth): expand this alongside the login/register pages.
 * Kept minimal for now: just where the JWT lives on the client.
 */

const TOKEN_KEY = "access_token";

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function isLoggedIn(): boolean {
  return getToken() !== null;
}
