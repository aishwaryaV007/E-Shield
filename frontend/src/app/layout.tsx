import "./globals.css";

export const metadata = {
  title: "ExamShield — AI Answer-Sheet Evaluator",
  description: "Upload a handwritten answer script and get AI-graded marks.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
