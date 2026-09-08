import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Store",
  description: "Customizable e-commerce platform",
};

// TODO (section 16 - Global Layout): replace this bare shell with
// Navbar + Footer + main content container, fed by GET /api/v1/store/settings.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
