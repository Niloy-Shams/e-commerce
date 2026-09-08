import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Bound to CSS variables so admin-configured StoreSettings
        // (primary_color / secondary_color) can theme the storefront
        // at runtime without a rebuild. Set the variables in layout.tsx
        // once GET /api/v1/store/settings is wired up (section 34).
        brand: {
          primary: "var(--store-primary, #1f2937)",
          secondary: "var(--store-secondary, #6b7280)",
        },
      },
    },
  },
  plugins: [],
};

export default config;
