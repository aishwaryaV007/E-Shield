"use client";
import { useState, useEffect, useRef } from "react";

type Answer = {
  question_no: string; type: string; student_answer: string; answer_key: string;
  predicted_mark: number; max_marks: number; percent: number; similarity: number;
  ocr_confidence: number; feedback: string; deduction_reasons: string[]; low_confidence: boolean;
};
type Sheet = {
  script_id: string; total_marks: number; max_total: number; percentage: number;
  low_confidence_count: number; elapsed_seconds?: number;
  mcq_marks: number; mcq_max: number; descriptive_marks: number; descriptive_max: number;
  answers: Answer[];
};
type Status = "idle" | "grading" | "done" | "error";
type Student = {
  id: string; name: string; roll: string; file: File | null;
  sheet: Sheet | null; status: Status; error: string; elapsed: number;
  edits: Record<string, string>;
};

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
let SEQ = 1;
const newStudent = (): Student =>
  ({ id: `s${SEQ}`, name: `Student ${SEQ++}`, roll: "", file: null, sheet: null,
     status: "idle", error: "", elapsed: 0, edits: {} });

const pctColor = (p: number) => (p >= 75 ? "var(--success)" : p >= 40 ? "var(--warn)" : "var(--danger)");
const half = (n: number) => (Math.round(n * 2) / 2).toString();  // 12 / 12.5 / 13
function gradeBand(p: number): { g: string; c: string } {
  if (p >= 90) return { g: "A+", c: "#059669" };
  if (p >= 80) return { g: "A", c: "#16a34a" };
  if (p >= 70) return { g: "B", c: "#2563eb" };
  if (p >= 60) return { g: "C", c: "#7c3aed" };
  if (p >= 50) return { g: "D", c: "#d97706" };
  if (p >= 40) return { g: "E", c: "#ea580c" };
  return { g: "F", c: "#dc2626" };
}

export default function Home() {
  const [keyFile, setKeyFile] = useState<File | null>(null);
  const [qpFile, setQpFile] = useState<File | null>(null);
  const [students, setStudents] = useState<Student[]>([newStudent()]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const ticker = useRef<any>(null);

  const patch = (id: string, p: Partial<Student>) =>
    setStudents((xs) => xs.map((s) => (s.id === id ? { ...s, ...p } : s)));

  // live elapsed ticker for any grading student
  useEffect(() => {
    const anyGrading = students.some((s) => s.status === "grading");
    if (anyGrading && !ticker.current) {
      ticker.current = setInterval(() =>
        setStudents((xs) => xs.map((s) => s.status === "grading" ? { ...s, elapsed: +(s.elapsed + 0.1).toFixed(1) } : s)), 100);
    } else if (!anyGrading && ticker.current) {
      clearInterval(ticker.current); ticker.current = null;
    }
    return () => { if (ticker.current) { clearInterval(ticker.current); ticker.current = null; } };
  }, [students]);

  async function gradeOne(id: string) {
    const st = students.find((s) => s.id === id);
    if (!st?.file) return;
    patch(id, { status: "grading", error: "", elapsed: 0 });
    try {
      const fd = new FormData();
      fd.append("file", st.file); fd.append("max_marks", "2");
      if (keyFile) fd.append("answer_key", keyFile);
      if (qpFile) fd.append("question_paper", qpFile);
      const res = await fetch(`${API}/api/v1/grade`, { method: "POST", body: fd });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `HTTP ${res.status}`);
      const sheet: Sheet = await res.json();
      patch(id, { status: "done", sheet, edits: Object.fromEntries(sheet.answers.map((a) => [a.question_no, a.student_answer])) });
    } catch (e: any) {
      patch(id, { status: "error", error: e.message || "Grading failed" });
    }
  }

  async function gradeAll() {
    for (const s of students) if (s.file && s.status !== "done") await gradeOne(s.id);
  }

  async function regrade(id: string) {
    const st = students.find((s) => s.id === id);
    if (!st?.sheet) return;
    patch(id, { status: "grading" });
    try {
      const body = {
        script_id: st.name + " (corrected)",
        answers: st.sheet.answers.map((a) => ({
          question_no: a.question_no, type: a.type,
          student_answer: st.edits[a.question_no] ?? a.student_answer,
          answer_key: a.answer_key, max_marks: a.max_marks,
        })),
      };
      const res = await fetch(`${API}/api/v1/rescore`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const sheet: Sheet = await res.json();
      patch(id, { status: "done", sheet });
    } catch (e: any) {
      patch(id, { status: "error", error: e.message || "Re-grade failed" });
    }
  }

  const graded = students.filter((s) => s.status === "done" && s.sheet);
  const selected = students.find((s) => s.id === selectedId) || null;

  const pcts = graded.map((s) => s.sheet!.percentage);
  const stats = pcts.length ? {
    avg: pcts.reduce((a, b) => a + b, 0) / pcts.length,
    hi: Math.max(...pcts), lo: Math.min(...pcts),
    pass: pcts.filter((p) => p >= 40).length,
  } : null;

  function exportCSV() {
    const head = ["Name", "Roll No", "MCQ", "MCQ Max", "Descriptive", "Desc Max", "Total", "Max", "Percentage", "Grade"];
    const rows = graded.map((s) => {
      const h = s.sheet!;
      return [s.name, s.roll, h.mcq_marks, h.mcq_max, h.descriptive_marks, h.descriptive_max,
              h.total_marks, h.max_total, h.percentage, gradeBand(h.percentage).g];
    });
    const csv = [head, ...rows].map((r) => r.map((x) => `"${String(x).replace(/"/g, '""')}"`).join(",")).join("\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    const a = document.createElement("a"); a.href = url; a.download = "examshield_results.csv"; a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-inner">
          <div className="brand"><span className="brand-badge">🛡️</span>
            ExamShield <span className="brand-sub">AI Answer-Sheet Evaluator</span></div>
          <span className="nav-pill">● Offline · No LLM grading</span>
        </div>
      </nav>

      <div className="container">
        {selected ? <Detail student={selected} onBack={() => setSelectedId(null)}
                            onEdit={(q, v) => patch(selected.id, { edits: { ...selected.edits, [q]: v } })}
                            onRegrade={() => regrade(selected.id)} /> : (
          <>
            <p className="lead">
              Build a class roster, then grade every student's handwritten script against a shared
              question paper &amp; answer key. Add students, rename them, upload PDFs, and grade all at once.
            </p>

            {/* shared exam files */}
            <div className="card card-pad" style={{ marginBottom: 20 }}>
              <h2 className="section-title">Exam files (shared by all students)</h2>
              <div className="field">
                <label>Answer key <span className="hint">— .txt or .csv (optional; default used if omitted)</span></label>
                <input className="file" type="file" accept=".txt,.csv" onChange={(e) => setKeyFile(e.target.files?.[0] || null)} />
                {keyFile && <span className="chip-ok">✓ {keyFile.name}</span>}
              </div>
              <div className="field">
                <label>Question paper <span className="hint">— .txt (optional; sets per-question max marks)</span></label>
                <input className="file" type="file" accept=".txt,.csv" onChange={(e) => setQpFile(e.target.files?.[0] || null)} />
                {qpFile && <span className="chip-ok">✓ {qpFile.name}</span>}
              </div>
            </div>

            {/* class statistics */}
            {stats && (
              <>
                <h2 className="section-title">Class summary ({graded.length} graded)</h2>
                <div className="stats" style={{ marginBottom: 20 }}>
                  <div className="stat hi"><div className="k">Class average</div>
                    <div className="v" style={{ color: pctColor(stats.avg) }}>{stats.avg.toFixed(1)}%</div></div>
                  <div className="stat"><div className="k">Highest</div><div className="v small" style={{ color: "var(--success)" }}>{stats.hi}%</div></div>
                  <div className="stat"><div className="k">Lowest</div><div className="v small" style={{ color: pctColor(stats.lo) }}>{stats.lo}%</div></div>
                  <div className="stat"><div className="k">Passed (≥40%)</div><div className="v small">{stats.pass} / {graded.length}</div></div>
                </div>
              </>
            )}

            {/* roster */}
            <h2 className="section-title">Students ({students.length})</h2>
            <div className="card">
              <div className="table-wrap">
                <table className="grades">
                  <thead><tr><th>Name</th><th>Roll no.</th><th>Answer script (PDF)</th><th>Result</th><th></th></tr></thead>
                  <tbody>
                    {students.map((s) => (
                      <tr key={s.id}>
                        <td style={{ minWidth: 180 }}>
                          <input className="inp-name" value={s.name}
                            onChange={(e) => patch(s.id, { name: e.target.value })} />
                        </td>
                        <td><input className="inp-roll" placeholder="—" value={s.roll}
                            onChange={(e) => patch(s.id, { roll: e.target.value })} /></td>
                        <td style={{ minWidth: 200 }}>
                          {s.file ? (
                            <span className="file-chosen">
                              📄 {s.file.name}
                              <button className="link" style={{ marginLeft: 8 }}
                                onClick={() => patch(s.id, { file: null, sheet: null, status: "idle" })}>change</button>
                            </span>
                          ) : (
                            <input className="file-sm" type="file" accept="application/pdf"
                              onChange={(e) => patch(s.id, { file: e.target.files?.[0] || null, status: "idle", sheet: null })} />
                          )}
                        </td>
                        <td>
                          {s.status === "idle" && <span className="status st-idle">{s.file ? "ready" : "no file"}</span>}
                          {s.status === "grading" && <span className="status st-grading">⏱ grading… {s.elapsed.toFixed(1)}s</span>}
                          {s.status === "error" && <span className="status st-error" title={s.error}>error</span>}
                          {s.status === "done" && s.sheet && (
                            <span className="result-cell">
                              <span className="score-pill" style={{ color: pctColor(s.sheet.percentage) }}>
                                {half(s.sheet.total_marks)}/{s.sheet.max_total} · {s.sheet.percentage}%
                              </span>
                              <span className="grade-badge" style={{ background: gradeBand(s.sheet.percentage).c }}>
                                {gradeBand(s.sheet.percentage).g}
                              </span>
                            </span>)}
                        </td>
                        <td style={{ whiteSpace: "nowrap", textAlign: "right" }}>
                          {s.status === "done"
                            ? <button className="link" onClick={() => setSelectedId(s.id)}>View / edit →</button>
                            : <button className="btn btn-primary btn-sm" disabled={!s.file || s.status === "grading"}
                                      onClick={() => gradeOne(s.id)}>Grade</button>}
                          {students.length > 1 &&
                            <button className="iconbtn" title="Remove"
                              onClick={() => setStudents((xs) => xs.filter((x) => x.id !== s.id))}>✕</button>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="toolbar">
              <button className="btn btn-ghost btn-sm" onClick={() => setStudents((xs) => [...xs, newStudent()])}>+ Add student</button>
              <button className="btn btn-primary btn-sm"
                onClick={gradeAll} disabled={!students.some((s) => s.file && s.status !== "done")}>
                Grade all
              </button>
              {graded.length > 0 &&
                <button className="btn btn-ghost btn-sm" onClick={exportCSV}>⬇ Export results (CSV)</button>}
              <span className="spacer" />
              {graded.length > 0 && <span className="count">{graded.length} of {students.length} graded</span>}
            </div>

            {error && <div className="alert alert-error" style={{ marginTop: 16 }}>⚠️ {error}</div>}
          </>
        )}
      </div>
    </>
  );
}

/* ── per-student detailed evaluated sheet ── */
function Detail({ student, onBack, onEdit, onRegrade }: {
  student: Student; onBack: () => void; onEdit: (q: string, v: string) => void; onRegrade: () => void;
}) {
  const s = student.sheet!;
  return (
    <>
      <button className="back" onClick={onBack}>← Back to roster</button>
      <h2 className="section-title">{student.name}{student.roll && ` · ${student.roll}`}</h2>
      <div className="stats" style={{ marginBottom: 20 }}>
        <div className="stat hi"><div className="k">Percentage</div>
          <div className="v" style={{ color: pctColor(s.percentage), display: "flex", alignItems: "center" }}>
            {s.percentage}%
            <span className="grade-badge" style={{ background: gradeBand(s.percentage).c }}>{gradeBand(s.percentage).g}</span>
          </div></div>
        <div className="stat"><div className="k">Total marks</div>
          <div className="v">{half(s.total_marks)}<span style={{ color: "var(--faint)", fontWeight: 500 }}> / {s.max_total}</span></div></div>
        {s.mcq_max > 0 && <div className="stat"><div className="k">MCQs</div><div className="v small">{s.mcq_marks} / {s.mcq_max}</div></div>}
        <div className="stat"><div className="k">Descriptive</div><div className="v small">{s.descriptive_marks} / {s.descriptive_max}</div></div>
        {s.elapsed_seconds != null && <div className="stat"><div className="k">⏱ Time</div><div className="v small">{s.elapsed_seconds}s</div></div>}
      </div>

      {s.low_confidence_count > 0 &&
        <div style={{ marginBottom: 16 }}><span className="alert-warn">⚑ {s.low_confidence_count} low-confidence answer(s) — verify below</span></div>}

      <div className="card">
        <div className="table-wrap">
          <table className="grades">
            <thead><tr><th>Q</th><th>Mark</th><th>OCR conf.</th>
              <th>Extracted answer — edit to correct</th><th>Correct answer (key)</th></tr></thead>
            <tbody>
              {s.answers.map((a) => (
                <tr key={a.question_no} className={a.low_confidence ? "warn" : ""}>
                  <td><div className="qno">Q{a.question_no}</div>
                    <span className={`qtype ${a.type}`}>{a.type === "mcq" ? "MCQ" : "Written"}</span></td>
                  <td><div className="mark">{a.predicted_mark}<span className="of"> / {a.max_marks}</span></div>
                    <div className="meter"><i style={{ width: `${Math.round((a.predicted_mark / a.max_marks) * 100)}%`,
                      background: pctColor((a.predicted_mark / a.max_marks) * 100) }} /></div></td>
                  <td className={`conf ${a.low_confidence ? "low" : ""}`}>{(a.ocr_confidence * 100).toFixed(0)}%{a.low_confidence && " ⚑"}</td>
                  <td style={{ minWidth: 280 }}>
                    {a.type === "mcq"
                      ? <select className="inp" value={student.edits[a.question_no] ?? a.student_answer}
                          onChange={(e) => onEdit(a.question_no, e.target.value)}>
                          <option value="">—</option>{["A", "B", "C", "D"].map((o) => <option key={o} value={o}>{o}</option>)}</select>
                      : <textarea className="inp" rows={3} value={student.edits[a.question_no] ?? a.student_answer}
                          onChange={(e) => onEdit(a.question_no, e.target.value)} />}
                  </td>
                  <td className={`keytext ${a.type}`} style={{ minWidth: 240, maxWidth: 340 }}>{a.answer_key}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="btn-row">
        <button className="btn btn-success" onClick={onRegrade} disabled={student.status === "grading"}>
          {student.status === "grading" ? "Re-grading…" : "✎ Re-grade with my corrections"}
        </button>
        <span className="muted-note">Fix any mis-read answer, then re-grade instantly (no OCR re-run).</span>
      </div>
      <p className="footnote">Marks come from the trained model (XGBoost) — never an LLM. Amber rows have low OCR confidence.</p>
    </>
  );
}
