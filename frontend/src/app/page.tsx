"use client";
import { useState } from "react";

type Answer = {
  question_no: string;
  student_answer: string;
  predicted_mark: number;
  max_marks: number;
  percent: number;
  similarity: number;
  feedback: string;
  deduction_reasons: string[];
  low_confidence: boolean;
};
type Sheet = {
  script_id: string;
  total_marks: number;
  max_total: number;
  percentage: number;
  low_confidence_count: number;
  answers: Answer[];
};

const C = {
  card: { background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155" } as React.CSSProperties,
  th: { textAlign: "left", padding: "8px 10px", color: "#94a3b8", fontSize: 13, borderBottom: "1px solid #334155" } as React.CSSProperties,
  td: { padding: "8px 10px", borderBottom: "1px solid #24324a", verticalAlign: "top" } as React.CSSProperties,
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sheet, setSheet] = useState<Sheet | null>(null);

  async function grade() {
    if (!file) return;
    setLoading(true); setError(""); setSheet(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      fd.append("max_marks", "2");
      // Call the backend directly (CORS-enabled); avoids the Next dev-proxy timeout on ~40s grading.
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API}/api/v1/grade`, { method: "POST", body: fd });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `HTTP ${res.status}`);
      setSheet(await res.json());
    } catch (e: any) {
      setError(e.message || "Grading failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: "40px 20px" }}>
      <h1 style={{ fontSize: 28, marginBottom: 4 }}>🛡️ ExamShield</h1>
      <p style={{ color: "#94a3b8", marginTop: 0 }}>
        Upload a handwritten answer script (PDF). The AI reads it, matches each answer to the key,
        and the trained model assigns marks.
      </p>

      <div style={{ ...C.card, marginBottom: 24 }}>
        <input type="file" accept="application/pdf"
               onChange={(e) => setFile(e.target.files?.[0] || null)}
               style={{ color: "#e2e8f0" }} />
        <button onClick={grade} disabled={!file || loading}
                style={{ marginLeft: 12, padding: "8px 18px", borderRadius: 8, border: "none",
                         background: loading ? "#475569" : "#3b82f6", color: "#fff",
                         cursor: file && !loading ? "pointer" : "not-allowed", fontWeight: 600 }}>
          {loading ? "Grading… (~40s)" : "Grade script"}
        </button>
        {file && <span style={{ marginLeft: 12, color: "#94a3b8" }}>{file.name}</span>}
      </div>

      {error && <div style={{ ...C.card, borderColor: "#ef4444", color: "#fca5a5", marginBottom: 24 }}>⚠️ {error}</div>}

      {sheet && (
        <>
          <div style={{ ...C.card, marginBottom: 20, display: "flex", gap: 32, alignItems: "center" }}>
            <div>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>Script</div>
              <div style={{ fontSize: 20, fontWeight: 700 }}>{sheet.script_id}</div>
            </div>
            <div>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>Total</div>
              <div style={{ fontSize: 20, fontWeight: 700 }}>{sheet.total_marks} / {sheet.max_total}</div>
            </div>
            <div>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>Percentage</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: "#34d399" }}>{sheet.percentage}%</div>
            </div>
            {sheet.low_confidence_count > 0 && (
              <div style={{ color: "#fbbf24" }}>⚑ {sheet.low_confidence_count} low-confidence — verify</div>
            )}
          </div>

          <div style={{ ...C.card, overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
              <thead>
                <tr>
                  <th style={C.th}>Q</th><th style={C.th}>Mark</th><th style={C.th}>Match</th>
                  <th style={C.th}>Extracted answer</th><th style={C.th}>Feedback</th>
                </tr>
              </thead>
              <tbody>
                {sheet.answers.map((a) => (
                  <tr key={a.question_no}>
                    <td style={C.td}><b>Q{a.question_no}</b></td>
                    <td style={{ ...C.td, whiteSpace: "nowrap", fontWeight: 700 }}>{a.predicted_mark}/{a.max_marks}</td>
                    <td style={{ ...C.td, color: a.similarity < 0.2 ? "#f87171" : "#94a3b8" }}>{a.similarity.toFixed(2)}</td>
                    <td style={{ ...C.td, color: "#cbd5e1", maxWidth: 340 }}>{a.student_answer.slice(0, 140)}</td>
                    <td style={{ ...C.td, color: "#94a3b8" }}>
                      {a.feedback}
                      {a.low_confidence && <span style={{ color: "#fbbf24" }}> ⚑</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p style={{ color: "#64748b", fontSize: 12, marginTop: 12 }}>
            Marks are produced by the trained model (XGBoost), never by an LLM. Low-confidence
            answers (⚑) are flagged for human verification.
          </p>
        </>
      )}
    </main>
  );
}
