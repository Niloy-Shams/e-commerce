"use client";

import { useEffect, useState } from "react";

type HealthState = "checking" | "ok" | "down";

// TODO (section 17 - Homepage): replace this with Hero, store description,
// featured products, categories, and a call-to-action, all sourced from
// the backend rather than hardcoded here.
export default function HomePage() {
  const [health, setHealth] = useState<HealthState>("checking");
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

  useEffect(() => {
    let cancelled = false;

    fetch(`${apiUrl}/health`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res.status)))
      .then((data) => {
        if (!cancelled) setHealth(data?.status === "ok" ? "ok" : "down");
      })
      .catch(() => {
        if (!cancelled) setHealth("down");
      });

    return () => {
      cancelled = true;
    };
  }, [apiUrl]);

  return (
    <main className="mx-auto flex min-h-screen max-w-xl flex-col justify-center px-6 py-16">
      <h1 className="text-2xl font-semibold text-gray-900">Project scaffold is running</h1>
      <p className="mt-2 text-gray-600">
        This page will become the storefront homepage. For now it confirms the frontend
        can reach the backend through Docker.
      </p>

      <div className="mt-8 flex items-center gap-3 rounded-lg border border-gray-200 px-4 py-3">
        <span
          className={`h-2.5 w-2.5 rounded-full ${
            health === "ok" ? "bg-green-500" : health === "down" ? "bg-red-500" : "bg-gray-300"
          }`}
        />
        <span className="text-sm text-gray-700">
          {health === "checking" && "Checking backend connection..."}
          {health === "ok" && `Backend reachable at ${apiUrl}`}
          {health === "down" && `Could not reach backend at ${apiUrl}`}
        </span>
      </div>

      <p className="mt-6 text-sm text-gray-500">
        Backend API docs: <code className="text-gray-700">http://localhost:8000/docs</code>
      </p>
    </main>
  );
}
