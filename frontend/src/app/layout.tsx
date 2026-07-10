import "./globals.css";

export const metadata = {
  title: "ExamShield — AI Answer-Sheet Evaluator",
  description: "Upload a handwritten answer script and get AI-graded marks.",
};

export const viewport = { width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
