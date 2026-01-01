import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HACKER MODE: ACTIVATED",
  description: "Юмористический лендинг в хакерском стиле",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>
        {children}
      </body>
    </html>
  );
}
