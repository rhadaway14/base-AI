import type { ReactNode } from "react";
import "./styles.css";

export const metadata = { title: "Architected AI Starter" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
