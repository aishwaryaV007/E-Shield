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
  mcq_marks: number;
  mcq_max: number;
  descriptive_marks: number;
  descriptive_max: number;
  answers: Answer[];
};

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

  useEffect(() => {
    if (loading) {
      setElapsed(0);
      timer.current = setInterval(() => setElapsed((s) => +(s + 0.1).toFixed(1)), 100);
    } else if (timer.current) clearInterval(timer.current);
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
      const res = await fetch(`${API}/api/v1/grade`, { method: "POST", body: fd });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `HTTP ${res.status}`);
      applySheet(await res.json());
    } catch (e: any) {
      setError(e.message || "Grading failed");
    } finally {
      setLoading(false);
    }
  }

  async function regrade() {
    if (!sheet) return;
    setRegrading(true); setError("");
    try {
      const body = {
        script_id: sheet.script_id + " (corrected)",
        answers: sheet.answers.map((a) => ({
          question_no: a.question_no, type: a.type,
          student_answer: edits[a.question_no] ?? a.student_answer,
          answer_key: a.answer_key, max_marks: a.max_marks,
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

  const pctColor = (p: number) => (p >= 75 ? "var(--success)" : p >= 40 ? "var(--warn)" : "var(--danger)");

  return (
    <>
      <nav className="navbar">
        <div className="navbar-inner">
          <div className="brand">
            <span className="brand-badge">🛡️</span>
            ExamShield <span className="brand-sub">AI Answer-Sheet Evaluator</span>
          </div>
          <span className="nav-pill">● Offline · No LLM grading</span>
        </div>
      </nav>

      <div className="container">
        <p className="lead">
          Upload a handwritten answer script and its question paper &amp; answer key. The AI reads the
          handwriting, matches each answer to the key, and a trained model assigns the marks.
        </p>

        {/* Upload panel */}
        <div className="card card-pad" style={{ marginBottom: 24 }}>
          <h2 className="section-title">1 · Upload</h2>
          <div className="field">
            <label>Student answer script <span className="req">(PDF, required)</span></label>
            <input className="file" type="file" accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)} />
            {file && <span className="chip-ok">✓ {file.name}</span>}
          </div>
          <div className="field">
            <label>Answer key <span className="hint">— .txt or .csv (optional; uses default if omitted)</span></label>
            <input className="file" type="file" accept=".txt,.csv"
              onChange={(e) => setKeyFile(e.target.files?.[0] || null)} />
            {keyFile && <span className="chip-ok">✓ {keyFile.name}</span>}
          </div>
          <div className="field">
            <label>Question paper <span className="hint">— .txt (optional; sets per-question max marks)</span></label>
            <input className="file" type="file" accept=".txt,.csv"
              onChange={(e) => setQpFile(e.target.files?.[0] || null)} />
            {qpFile && <span className="chip-ok">✓ {qpFile.name}</span>}
          </div>
          <div className="btn-row">
            <button className="btn btn-primary" onClick={grade} disabled={!file || loading}>
              {loading ? `⏱ Grading… ${elapsed.toFixed(1)}s` : "Grade script"}
            </button>
            {loading && <span className="muted-note">reading handwriting + scoring — usually 30–45s</span>}
          </div>
        </div>

        {error && <div className="alert alert-error">⚠️ {error}</div>}

        {sheet && (
          <>
            <h2 className="section-title">2 · Result — {sheet.script_id}</h2>
            <div className="stats" style={{ marginBottom: 20 }}>
              <div className="stat hi">
                <div className="k">Percentage</div>
                <div className="v" style={{ color: pctColor(sheet.percentage) }}>{sheet.percentage}%</div>
              </div>
              <div className="stat">
                <div className="k">Total marks</div>
                <div className="v">{sheet.total_marks}<span className="of" style={{ color: "var(--faint)", fontWeight: 500 }}> / {sheet.max_total}</span></div>
              </div>
              {sheet.mcq_max > 0 && (
                <div className="stat"><div className="k">MCQs</div><div className="v small">{sheet.mcq_marks} / {sheet.mcq_max}</div></div>
              )}
              <div className="stat"><div className="k">Descriptive</div><div className="v small">{sheet.descriptive_marks} / {sheet.descriptive_max}</div></div>
              {sheet.elapsed_seconds != null && (
                <div className="stat"><div className="k">⏱ Time</div><div className="v small">{sheet.elapsed_seconds}s</div></div>
              )}
            </div>

            {sheet.low_confidence_count > 0 && (
              <div style={{ marginBottom: 16 }}>
                <span className="alert-warn">⚑ {sheet.low_confidence_count} low-confidence answer(s) — verify &amp; correct below</span>
              </div>
            )}

            <div className="card">
              <div className="table-wrap">
                <table className="grades">
                  <thead>
                    <tr>
                      <th>Q</th><th>Mark</th><th>OCR conf.</th>
                      <th>Extracted answer — edit to correct</th><th>Correct answer (key)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sheet.answers.map((a) => (
                      <tr key={a.question_no} className={a.low_confidence ? "warn" : ""}>
                        <td>
                          <div className="qno">Q{a.question_no}</div>
                          <span className={`qtype ${a.type}`}>{a.type === "mcq" ? "MCQ" : "Written"}</span>
                        </td>
                        <td>
                          <div className="mark">{a.predicted_mark}<span className="of"> / {a.max_marks}</span></div>
                          <div className="meter"><i style={{ width: `${Math.round((a.predicted_mark / a.max_marks) * 100)}%`, background: pctColor((a.predicted_mark / a.max_marks) * 100) }} /></div>
                        </td>
                        <td className={`conf ${a.low_confidence ? "low" : ""}`}>
                          {(a.ocr_confidence * 100).toFixed(0)}%{a.low_confidence && " ⚑"}
                        </td>
                        <td style={{ minWidth: 280 }}>
                          {a.type === "mcq" ? (
                            <select className="inp" value={edits[a.question_no] ?? a.student_answer}
                              onChange={(e) => setEdits((p) => ({ ...p, [a.question_no]: e.target.value }))}>
                              <option value="">—</option>
                              {["A", "B", "C", "D"].map((o) => <option key={o} value={o}>{o}</option>)}
                            </select>
                          ) : (
                            <textarea className="inp" rows={3} value={edits[a.question_no] ?? a.student_answer}
                              onChange={(e) => setEdits((p) => ({ ...p, [a.question_no]: e.target.value }))} />
                          )}
                        </td>
                        <td className={`keytext ${a.type}`} style={{ minWidth: 240, maxWidth: 340 }}>{a.answer_key}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="btn-row">
              <button className="btn btn-success" onClick={regrade} disabled={regrading}>
                {regrading ? "Re-grading…" : "✎ Re-grade with my corrections"}
              </button>
              <span className="muted-note">Fix any mis-read answer above, then re-grade instantly (no OCR re-run).</span>
            </div>
            <p className="footnote">
              Marks come from the trained model (XGBoost) — never an LLM. Amber rows have low OCR
              confidence; verify and correct them before publishing.
            </p>
          </>
        )}
      </div>
    </>
  );
}
