"use client";
import { useState, useEffect, useRef } from "react";

type Answer = {
  question_no: string;
  type: string;
  student_answer: string;
  answer_key: string;
  predicted_mark: number;
  max_marks: number;
  percent: number;
  similarity: number;
  ocr_confidence: number;
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
  elapsed_seconds?: number;
  answers: Answer[];
};

const C = {
  card: { background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155" } as React.CSSProperties,
  th: { textAlign: "left", padding: "8px 10px", color: "#94a3b8", fontSize: 13, borderBottom: "1px solid #334155" } as React.CSSProperties,
  td: { padding: "8px 10px", borderBottom: "1px solid #24324a", verticalAlign: "top" } as React.CSSProperties,
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [keyFile, setKeyFile] = useState<File | null>(null);
  const [qpFile, setQpFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sheet, setSheet] = useState<Sheet | null>(null);
  const [edits, setEdits] = useState<Record<string, string>>({});
  const [regrading, setRegrading] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const timer = useRef<any>(null);

  function applySheet(s: Sheet) {
    setSheet(s);
    setEdits(Object.fromEntries(s.answers.map((a) => [a.question_no, a.student_answer])));
  }

  async function regrade() {
    if (!sheet) return;
    setRegrading(true); setError("");
    try {
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const body = {
        script_id: sheet.script_id + " (corrected)",
        answers: sheet.answers.map((a) => ({
          question_no: a.question_no,
          type: a.type,
          student_answer: edits[a.question_no] ?? a.student_answer,
          answer_key: a.answer_key,
          max_marks: a.max_marks,
        })),
      };
      const res = await fetch(`${API}/api/v1/rescore`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      applySheet(await res.json());
    } catch (e: any) {
      setError(e.message || "Re-grade failed");
    } finally {
      setRegrading(false);
    }
  }

  // live seconds counter while grading
  useEffect(() => {
    if (loading) {
      setElapsed(0);
      timer.current = setInterval(() => setElapsed((s) => +(s + 0.1).toFixed(1)), 100);
    } else if (timer.current) {
      clearInterval(timer.current);
    }
    return () => timer.current && clearInterval(timer.current);
  }, [loading]);

  async function grade() {
    if (!file) return;
    setLoading(true); setError(""); setSheet(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      fd.append("max_marks", "2");
      if (keyFile) fd.append("answer_key", keyFile);
      if (qpFile) fd.append("question_paper", qpFile);
      // Call the backend directly (CORS-enabled); avoids the Next dev-proxy timeout on ~40s grading.
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API}/api/v1/grade`, { method: "POST", body: fd });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `HTTP ${res.status}`);
      applySheet(await res.json());
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
        <div style={{ marginBottom: 12 }}>
          <label style={{ display: "block", fontSize: 13, color: "#94a3b8", marginBottom: 4 }}>
            Student answer script (PDF) *
          </label>
          <input type="file" accept="application/pdf"
                 onChange={(e) => setFile(e.target.files?.[0] || null)}
                 style={{ color: "#e2e8f0" }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: "block", fontSize: 13, color: "#94a3b8", marginBottom: 4 }}>
            Answer key (optional CSV: Question_Number,Type,Correct_Answer) — uses the default exam key if omitted
          </label>
          <input type="file" accept=".txt,.csv"
                 onChange={(e) => setKeyFile(e.target.files?.[0] || null)}
                 style={{ color: "#e2e8f0" }} />
          {keyFile && <span style={{ marginLeft: 10, color: "#34d399", fontSize: 13 }}>✓ {keyFile.name}</span>}
        </div>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: "block", fontSize: 13, color: "#94a3b8", marginBottom: 4 }}>
            Question paper (optional) — the model reads per-question marks from it (e.g. "(2 Marks Each)", "[8]")
          </label>
          <input type="file" accept=".txt,.csv"
                 onChange={(e) => setQpFile(e.target.files?.[0] || null)}
                 style={{ color: "#e2e8f0" }} />
          {qpFile && <span style={{ marginLeft: 10, color: "#34d399", fontSize: 13 }}>✓ {qpFile.name}</span>}
        </div>
        <button onClick={grade} disabled={!file || loading}
                style={{ padding: "9px 20px", borderRadius: 8, border: "none",
                         background: loading ? "#475569" : "#3b82f6", color: "#fff",
                         cursor: file && !loading ? "pointer" : "not-allowed", fontWeight: 600 }}>
          {loading ? `⏱ Grading… ${elapsed.toFixed(1)}s` : "Grade script"}
        </button>
        {loading && <span style={{ marginLeft: 12, color: "#94a3b8", fontSize: 13 }}>
          reading handwriting + scoring — usually 30–45s
        </span>}
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
            {sheet.elapsed_seconds != null && (
              <div>
                <div style={{ fontSize: 13, color: "#94a3b8" }}>⏱ Time</div>
                <div style={{ fontSize: 20, fontWeight: 700 }}>{sheet.elapsed_seconds}s</div>
              </div>
            )}
            {sheet.low_confidence_count > 0 && (
              <div style={{ color: "#fbbf24" }}>⚑ {sheet.low_confidence_count} low-confidence — verify</div>
            )}
          </div>

          <div style={{ ...C.card, overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
              <thead>
                <tr>
                  <th style={C.th}>Q</th><th style={C.th}>Mark</th><th style={C.th}>OCR&nbsp;conf.</th>
                  <th style={C.th}>Extracted answer — edit to correct</th><th style={C.th}>Correct answer (key)</th>
                </tr>
              </thead>
              <tbody>
                {sheet.answers.map((a) => (
                  <tr key={a.question_no} style={a.low_confidence ? { background: "#2a2416" } : undefined}>
                    <td style={C.td}><b>Q{a.question_no}</b></td>
                    <td style={{ ...C.td, whiteSpace: "nowrap", fontWeight: 700 }}>{a.predicted_mark}/{a.max_marks}</td>
                    <td style={{ ...C.td, color: a.low_confidence ? "#fbbf24" : "#94a3b8", whiteSpace: "nowrap" }}>
                      {(a.ocr_confidence * 100).toFixed(0)}%{a.low_confidence && " ⚑"}
                    </td>
                    <td style={{ ...C.td, maxWidth: 340 }}>
                      {a.type === "mcq" ? (
                        <select
                          value={edits[a.question_no] ?? a.student_answer}
                          onChange={(e) => setEdits((p) => ({ ...p, [a.question_no]: e.target.value }))}
                          style={{ background: "#0f172a", color: "#e2e8f0", border: "1px solid #334155",
                                   borderRadius: 6, padding: "5px 8px", fontSize: 14 }}>
                          <option value="">—</option>
                          {["A", "B", "C", "D"].map((o) => <option key={o} value={o}>{o}</option>)}
                        </select>
                      ) : (
                        <textarea
                          value={edits[a.question_no] ?? a.student_answer}
                          onChange={(e) => setEdits((p) => ({ ...p, [a.question_no]: e.target.value }))}
                          rows={2}
                          style={{ width: "100%", background: "#0f172a", color: "#e2e8f0",
                                   border: "1px solid #334155", borderRadius: 6, padding: 6,
                                   fontSize: 13, fontFamily: "inherit", resize: "vertical" }} />
                      )}
                    </td>
                    <td style={{ ...C.td, color: "#86efac", maxWidth: 300 }}>
                      {a.type === "mcq" ? <b>{a.answer_key}</b> : a.answer_key}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 14 }}>
            <button onClick={regrade} disabled={regrading}
                    style={{ padding: "9px 20px", borderRadius: 8, border: "none",
                             background: regrading ? "#475569" : "#16a34a", color: "#fff",
                             cursor: regrading ? "not-allowed" : "pointer", fontWeight: 600 }}>
              {regrading ? "Re-grading…" : "✎ Re-grade with my corrections"}
            </button>
            <span style={{ color: "#64748b", fontSize: 12 }}>
              Fix any mis-read answer above, then re-grade instantly (no OCR re-run).
            </span>
          </div>
          <p style={{ color: "#64748b", fontSize: 12, marginTop: 12 }}>
            Marks come from the trained model (XGBoost), never an LLM. Highlighted rows have low OCR
            confidence (⚑) — verify and correct them before publishing.
          </p>
        </>
      )}
    </main>
  );
}
