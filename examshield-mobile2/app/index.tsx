import { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Platform,
  Share,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as DocumentPicker from 'expo-document-picker';
import {
  Answer,
  GradeSheet,
  PickedFile,
  gradeBand,
  gradeScript,
  rescore,
} from '../lib/api';

/* ── monochrome / serif / rectangular design tokens (mirrors web globals.css) ── */
const SERIF = Platform.select({ ios: 'Palatino', android: 'serif', default: 'serif' });
const C = {
  paper: '#ffffff',
  panel: '#ffffff',
  ink: '#111111',
  ink2: '#2b2b2b',
  border: '#dcdcdc',
  border2: '#bcbcbc',
  muted: '#6a6a6a',
  faint: '#9c9c9c',
  shade: '#f6f6f6',
  warnBg: '#f0f0f0',
};

type Status = 'idle' | 'grading' | 'done' | 'error';
type Student = {
  id: string;
  name: string;
  roll: string;
  file: PickedFile | null;
  sheet: GradeSheet | null;
  status: Status;
  error: string;
  elapsed: number;
  edits: Record<string, string>;
};

let SEQ = 1;
const newStudent = (): Student => ({
  id: `s${SEQ}`,
  name: `Student ${SEQ++}`,
  roll: '',
  file: null,
  sheet: null,
  status: 'idle',
  error: '',
  elapsed: 0,
  edits: {},
});

const half = (n: number) => (Math.round(n * 2) / 2).toString();

async function pickFile(types: string[]): Promise<PickedFile | null> {
  const r = await DocumentPicker.getDocumentAsync({ type: types, copyToCacheDirectory: true });
  if (r.canceled) return null;
  const a = r.assets[0];
  return { uri: a.uri, name: a.name, mimeType: a.mimeType || undefined };
}

const KEY_TYPES = ['text/plain', 'text/csv', 'text/comma-separated-values', 'application/vnd.ms-excel'];

export default function Home() {
  const [keyFile, setKeyFile] = useState<PickedFile | null>(null);
  const [qpFile, setQpFile] = useState<PickedFile | null>(null);
  const [students, setStudents] = useState<Student[]>([newStudent()]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const ticker = useRef<ReturnType<typeof setInterval> | null>(null);

  const patch = (id: string, p: Partial<Student>) =>
    setStudents((xs) => xs.map((s) => (s.id === id ? { ...s, ...p } : s)));

  // live elapsed ticker while any student is grading
  useEffect(() => {
    const anyGrading = students.some((s) => s.status === 'grading');
    if (anyGrading && !ticker.current) {
      ticker.current = setInterval(
        () =>
          setStudents((xs) =>
            xs.map((s) =>
              s.status === 'grading' ? { ...s, elapsed: +(s.elapsed + 0.1).toFixed(1) } : s
            )
          ),
        100
      );
    } else if (!anyGrading && ticker.current) {
      clearInterval(ticker.current);
      ticker.current = null;
    }
    return () => {
      if (ticker.current) {
        clearInterval(ticker.current);
        ticker.current = null;
      }
    };
  }, [students]);

  async function gradeOne(id: string) {
    const st = students.find((s) => s.id === id);
    if (!st?.file) return;
    patch(id, { status: 'grading', error: '', elapsed: 0 });
    try {
      const sheet = await gradeScript(st.file, {
        answerKey: keyFile || undefined,
        questionPaper: qpFile || undefined,
        maxMarks: 2,
      });
      patch(id, {
        status: 'done',
        sheet,
        edits: Object.fromEntries(sheet.answers.map((a) => [a.question_no, a.student_answer])),
      });
    } catch (e: any) {
      patch(id, {
        status: 'error',
        error: e?.response?.data?.detail || e?.message || 'Grading failed',
      });
    }
  }

  async function gradeAll() {
    for (const s of students) if (s.file && s.status !== 'done') await gradeOne(s.id);
  }

  async function regrade(id: string) {
    const st = students.find((s) => s.id === id);
    if (!st?.sheet) return;
    patch(id, { status: 'grading' });
    try {
      const answers = st.sheet.answers.map((a) => ({
        question_no: a.question_no,
        type: a.type,
        student_answer: st.edits[a.question_no] ?? a.student_answer,
        answer_key: a.answer_key,
        max_marks: a.max_marks,
      }));
      const sheet = await rescore(answers, `${st.name} (corrected)`);
      patch(id, { status: 'done', sheet });
    } catch (e: any) {
      patch(id, { status: 'error', error: e?.message || 'Re-grade failed' });
    }
  }

  const graded = students.filter((s) => s.status === 'done' && s.sheet);
  const selected = students.find((s) => s.id === selectedId) || null;

  const pcts = graded.map((s) => s.sheet!.percentage);
  const stats = pcts.length
    ? {
        avg: pcts.reduce((a, b) => a + b, 0) / pcts.length,
        hi: Math.max(...pcts),
        lo: Math.min(...pcts),
        pass: pcts.filter((p) => p >= 40).length,
      }
    : null;

  async function exportCSV() {
    const head = ['Name', 'Roll No', 'MCQ', 'MCQ Max', 'Descriptive', 'Desc Max', 'Total', 'Max', 'Percentage', 'Grade'];
    const rows = graded.map((s) => {
      const h = s.sheet!;
      return [s.name, s.roll, h.mcq_marks, h.mcq_max, h.descriptive_marks, h.descriptive_max, h.total_marks, h.max_total, h.percentage, gradeBand(h.percentage)];
    });
    const csv = [head, ...rows]
      .map((r) => r.map((x) => `"${String(x).replace(/"/g, '""')}"`).join(','))
      .join('\n');
    await Share.share({ message: csv, title: 'examshield_results.csv' });
  }

  return (
    <SafeAreaView style={styles.screen} edges={['top']}>
      {/* masthead */}
      <View style={styles.navbar}>
        <View style={styles.brand}>
          <View style={styles.brandBadge}>
            <Text style={styles.brandBadgeText}>E</Text>
          </View>
          <View>
            <Text style={styles.brandName}>ExamShield</Text>
            <Text style={styles.brandSub}>AI ANSWER-SHEET EVALUATOR</Text>
          </View>
        </View>
        <View style={styles.navPill}>
          <Text style={styles.navPillText}>OFFLINE · NO LLM</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.container}>
        {selected ? (
          <Detail
            student={selected}
            onBack={() => setSelectedId(null)}
            onEdit={(q, v) => patch(selected.id, { edits: { ...selected.edits, [q]: v } })}
            onRegrade={() => regrade(selected.id)}
          />
        ) : (
          <>
            <Text style={styles.lead}>
              Build a class roster, then grade every student's handwritten script against a shared
              question paper &amp; answer key. Add students, rename them, upload PDFs, and grade all at once.
            </Text>

            {/* shared exam files */}
            <View style={[styles.card, styles.cardPad, { marginBottom: 20 }]}>
              <SectionTitle>Exam files (shared by all students)</SectionTitle>
              <FileField
                label="Answer key"
                hint="— .txt or .csv (optional; default used if omitted)"
                file={keyFile}
                onPick={async () => setKeyFile((await pickFile(KEY_TYPES)) || keyFile)}
                onClear={() => setKeyFile(null)}
              />
              <FileField
                label="Question paper"
                hint="— .txt (optional; sets per-question max marks)"
                file={qpFile}
                onPick={async () => setQpFile((await pickFile(KEY_TYPES)) || qpFile)}
                onClear={() => setQpFile(null)}
              />
            </View>

            {/* class statistics */}
            {stats && (
              <>
                <SectionTitle>Class summary ({graded.length} graded)</SectionTitle>
                <View style={[styles.statsGrid, { marginBottom: 20 }]}>
                  <StatTile k="Class average" v={`${stats.avg.toFixed(1)}%`} big hi />
                  <StatTile k="Highest" v={`${stats.hi}%`} />
                  <StatTile k="Lowest" v={`${stats.lo}%`} />
                  <StatTile k="Passed (≥40%)" v={`${stats.pass} / ${graded.length}`} />
                </View>
              </>
            )}

            {/* roster */}
            <SectionTitle>Students ({students.length})</SectionTitle>
            {students.map((s) => (
              <StudentCard
                key={s.id}
                s={s}
                canRemove={students.length > 1}
                onName={(v) => patch(s.id, { name: v })}
                onRoll={(v) => patch(s.id, { roll: v })}
                onPick={async () => {
                  const f = await pickFile(['application/pdf']);
                  if (f) patch(s.id, { file: f, status: 'idle', sheet: null });
                }}
                onClearFile={() => patch(s.id, { file: null, sheet: null, status: 'idle' })}
                onGrade={() => gradeOne(s.id)}
                onView={() => setSelectedId(s.id)}
                onRemove={() => setStudents((xs) => xs.filter((x) => x.id !== s.id))}
              />
            ))}

            {/* toolbar */}
            <View style={styles.toolbar}>
              <TouchableOpacity
                style={[styles.btn, styles.btnGhost]}
                onPress={() => setStudents((xs) => [...xs, newStudent()])}
              >
                <Text style={styles.btnGhostText}>+ Add student</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.btn,
                  styles.btnPrimary,
                  !students.some((s) => s.file && s.status !== 'done') && styles.btnDisabled,
                ]}
                disabled={!students.some((s) => s.file && s.status !== 'done')}
                onPress={gradeAll}
              >
                <Text style={styles.btnPrimaryText}>Grade all</Text>
              </TouchableOpacity>
              {graded.length > 0 && (
                <TouchableOpacity style={[styles.btn, styles.btnGhost]} onPress={exportCSV}>
                  <Text style={styles.btnGhostText}>⬇ Export CSV</Text>
                </TouchableOpacity>
              )}
            </View>
            {graded.length > 0 && (
              <Text style={styles.count}>
                {graded.length} of {students.length} graded
              </Text>
            )}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

/* ── small building blocks ── */
function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <View style={styles.sectionTitleRow}>
      <Text style={styles.sectionTitle}>{children}</Text>
      <View style={styles.sectionRule} />
    </View>
  );
}

function FileField({
  label,
  hint,
  file,
  onPick,
  onClear,
}: {
  label: string;
  hint: string;
  file: PickedFile | null;
  onPick: () => void;
  onClear: () => void;
}) {
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>
        {label} <Text style={styles.fieldHint}>{hint}</Text>
      </Text>
      <View style={styles.fileRow}>
        <TouchableOpacity style={styles.chooseBtn} onPress={onPick}>
          <Text style={styles.chooseBtnText}>Choose File</Text>
        </TouchableOpacity>
        {file ? (
          <>
            <Text style={styles.chipOk} numberOfLines={1}>
              ✓ {file.name}
            </Text>
            <TouchableOpacity onPress={onClear}>
              <Text style={styles.link}>clear</Text>
            </TouchableOpacity>
          </>
        ) : (
          <Text style={styles.noFile}>No file chosen</Text>
        )}
      </View>
    </View>
  );
}

function StatTile({ k, v, big, hi }: { k: string; v: string; big?: boolean; hi?: boolean }) {
  return (
    <View style={[styles.statTile, hi && styles.statTileHi]}>
      {hi && <View style={styles.statAccent} />}
      <Text style={styles.statK}>{k.toUpperCase()}</Text>
      <Text style={[styles.statV, big ? styles.statVBig : styles.statVSmall]}>{v}</Text>
    </View>
  );
}

function StudentCard({
  s,
  canRemove,
  onName,
  onRoll,
  onPick,
  onClearFile,
  onGrade,
  onView,
  onRemove,
}: {
  s: Student;
  canRemove: boolean;
  onName: (v: string) => void;
  onRoll: (v: string) => void;
  onPick: () => void;
  onClearFile: () => void;
  onGrade: () => void;
  onView: () => void;
  onRemove: () => void;
}) {
  return (
    <View style={styles.card}>
      <View style={styles.studentCard}>
        <View style={styles.studentTop}>
          <TextInput style={styles.inpName} value={s.name} onChangeText={onName} />
          {canRemove && (
            <TouchableOpacity onPress={onRemove} style={styles.iconBtn}>
              <Text style={styles.iconBtnText}>✕</Text>
            </TouchableOpacity>
          )}
        </View>

        <View style={styles.rowLine}>
          <Text style={styles.colLabel}>ROLL NO.</Text>
          <TextInput
            style={styles.inpRoll}
            value={s.roll}
            onChangeText={onRoll}
            placeholder="—"
            placeholderTextColor={C.faint}
          />
        </View>

        <View style={styles.rowLine}>
          <Text style={styles.colLabel}>ANSWER SCRIPT (PDF)</Text>
          {s.file ? (
            <View style={styles.fileChosenRow}>
              <Text style={styles.fileChosen} numberOfLines={1}>
                📄 {s.file.name}
              </Text>
              <TouchableOpacity onPress={onClearFile}>
                <Text style={styles.link}>change</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.chooseBtnSm} onPress={onPick}>
              <Text style={styles.chooseBtnText}>Choose File</Text>
            </TouchableOpacity>
          )}
        </View>

        <View style={styles.studentBottom}>
          <View style={styles.resultArea}>
            {s.status === 'idle' && <StatusPill text={s.file ? 'READY' : 'NO FILE'} />}
            {s.status === 'grading' && (
              <StatusPill text={`⏱ GRADING… ${s.elapsed.toFixed(1)}s`} active />
            )}
            {s.status === 'error' && <StatusPill text="ERROR" active />}
            {s.status === 'done' && s.sheet && (
              <View style={styles.resultCell}>
                <Text style={styles.scorePill}>
                  {half(s.sheet.total_marks)}/{s.sheet.max_total} · {s.sheet.percentage}%
                </Text>
                <View style={styles.gradeBadge}>
                  <Text style={styles.gradeBadgeText}>{gradeBand(s.sheet.percentage)}</Text>
                </View>
              </View>
            )}
          </View>

          {s.status === 'done' ? (
            <TouchableOpacity onPress={onView}>
              <Text style={styles.link}>View / edit →</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[
                styles.btn,
                styles.btnPrimary,
                styles.btnSm,
                (!s.file || s.status === 'grading') && styles.btnDisabled,
              ]}
              disabled={!s.file || s.status === 'grading'}
              onPress={onGrade}
            >
              <Text style={styles.btnPrimaryText}>Grade</Text>
            </TouchableOpacity>
          )}
        </View>
        {s.status === 'error' && !!s.error && <Text style={styles.errorText}>{s.error}</Text>}
      </View>
    </View>
  );
}

function StatusPill({ text, active }: { text: string; active?: boolean }) {
  return (
    <View style={[styles.statusPill, active && styles.statusPillActive]}>
      <Text style={[styles.statusPillText, active && styles.statusPillTextActive]}>{text}</Text>
    </View>
  );
}

/* ── per-student detailed evaluated sheet ── */
function Detail({
  student,
  onBack,
  onEdit,
  onRegrade,
}: {
  student: Student;
  onBack: () => void;
  onEdit: (q: string, v: string) => void;
  onRegrade: () => void;
}) {
  const s = student.sheet!;
  return (
    <>
      <TouchableOpacity onPress={onBack}>
        <Text style={styles.back}>← Back to roster</Text>
      </TouchableOpacity>
      <SectionTitle>
        {student.name}
        {student.roll ? ` · ${student.roll}` : ''}
      </SectionTitle>

      <View style={[styles.statsGrid, { marginBottom: 20 }]}>
        <StatTile k="Percentage" v={`${s.percentage}% · ${gradeBand(s.percentage)}`} big hi />
        <StatTile k="Total marks" v={`${half(s.total_marks)} / ${s.max_total}`} />
        {s.mcq_max > 0 && <StatTile k="MCQs" v={`${s.mcq_marks} / ${s.mcq_max}`} />}
        <StatTile k="Descriptive" v={`${s.descriptive_marks} / ${s.descriptive_max}`} />
      </View>

      {s.low_confidence_count > 0 && (
        <View style={styles.alertWarn}>
          <Text style={styles.alertWarnText}>
            ⚑ {s.low_confidence_count} low-confidence answer(s) — verify below
          </Text>
        </View>
      )}

      {s.answers.map((a) => (
        <QuestionCard
          key={a.question_no}
          a={a}
          edit={student.edits[a.question_no] ?? a.student_answer}
          onEdit={(v) => onEdit(a.question_no, v)}
        />
      ))}

      <TouchableOpacity
        style={[
          styles.btn,
          styles.btnPrimary,
          { marginTop: 20 },
          student.status === 'grading' && styles.btnDisabled,
        ]}
        disabled={student.status === 'grading'}
        onPress={onRegrade}
      >
        {student.status === 'grading' ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.btnPrimaryText}>✎ Re-grade with my corrections</Text>
        )}
      </TouchableOpacity>
      <Text style={styles.footnote}>
        Fix any mis-read answer, then re-grade instantly (no OCR re-run). Marks come from the trained
        model (XGBoost) — never an LLM. Shaded rows have low OCR confidence.
      </Text>
    </>
  );
}

function QuestionCard({ a, edit, onEdit }: { a: Answer; edit: string; onEdit: (v: string) => void }) {
  const pct = Math.round((a.predicted_mark / a.max_marks) * 100);
  const isMcq = a.type === 'mcq';
  return (
    <View style={[styles.card, styles.qCard, a.low_confidence && styles.qCardWarn]}>
      <View style={styles.qHeader}>
        <View style={styles.qHeaderLeft}>
          <Text style={styles.qno}>Q{a.question_no}</Text>
          <View style={[styles.qtype, isMcq && styles.qtypeMcq]}>
            <Text style={[styles.qtypeText, isMcq && styles.qtypeTextMcq]}>
              {isMcq ? 'MCQ' : 'WRITTEN'}
            </Text>
          </View>
        </View>
        <View style={styles.qMarkWrap}>
          <Text style={styles.mark}>
            {a.predicted_mark}
            <Text style={styles.markOf}> / {a.max_marks}</Text>
          </Text>
          <View style={styles.meter}>
            <View style={[styles.meterFill, { width: `${pct}%` }]} />
          </View>
        </View>
      </View>

      <Text style={styles.qFieldLabel}>
        OCR CONFIDENCE:{' '}
        <Text style={a.low_confidence ? styles.confLow : styles.confOk}>
          {(a.ocr_confidence * 100).toFixed(0)}%{a.low_confidence ? ' ⚑' : ''}
        </Text>
      </Text>

      <Text style={styles.qFieldLabel}>EXTRACTED ANSWER — edit to correct:</Text>
      {isMcq ? (
        <View style={styles.mcqRow}>
          {['', 'A', 'B', 'C', 'D'].map((o) => (
            <TouchableOpacity
              key={o || 'none'}
              style={[styles.mcqOpt, edit === o && styles.mcqOptActive]}
              onPress={() => onEdit(o)}
            >
              <Text style={[styles.mcqOptText, edit === o && styles.mcqOptTextActive]}>
                {o || '—'}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      ) : (
        <TextInput style={styles.inpArea} value={edit} onChangeText={onEdit} multiline />
      )}

      <Text style={styles.qFieldLabel}>CORRECT ANSWER (KEY):</Text>
      <Text style={[styles.keyText, isMcq && styles.keyTextMcq]}>{a.answer_key || '—'}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: C.paper },
  container: { padding: 18, paddingBottom: 60 },

  /* masthead */
  navbar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 18,
    paddingVertical: 12,
    borderBottomWidth: 2,
    borderBottomColor: C.ink,
    backgroundColor: C.paper,
  },
  brand: { flexDirection: 'row', alignItems: 'center', gap: 10, flex: 1 },
  brandBadge: {
    width: 34,
    height: 34,
    borderRadius: 2,
    backgroundColor: C.ink,
    alignItems: 'center',
    justifyContent: 'center',
  },
  brandBadgeText: { color: '#fff', fontFamily: SERIF, fontWeight: '700', fontSize: 18 },
  brandName: { fontFamily: SERIF, fontWeight: '700', fontSize: 20, color: C.ink },
  brandSub: { fontSize: 9, letterSpacing: 1.4, color: C.muted, marginTop: 2 },
  navPill: { borderWidth: 1.5, borderColor: C.ink, paddingHorizontal: 8, paddingVertical: 5 },
  navPillText: { fontSize: 9, letterSpacing: 0.5, fontWeight: '700', color: C.ink },

  lead: { color: C.muted, marginBottom: 22, fontSize: 14.5, lineHeight: 21 },

  card: {
    backgroundColor: C.panel,
    borderWidth: 1,
    borderColor: C.ink,
    borderRadius: 2,
    marginBottom: 12,
  },
  cardPad: { padding: 18 },

  sectionTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 14,
    marginTop: 4,
  },
  sectionTitle: { fontFamily: SERIF, fontSize: 16, fontWeight: '700', color: C.ink },
  sectionRule: { flex: 1, height: 1, backgroundColor: C.border },

  /* file fields */
  field: { marginBottom: 16 },
  fieldLabel: { fontSize: 12.5, fontWeight: '700', color: C.ink2, marginBottom: 8 },
  fieldHint: { fontWeight: '400', color: C.faint },
  fileRow: { flexDirection: 'row', alignItems: 'center', gap: 10, flexWrap: 'wrap' },
  chooseBtn: { backgroundColor: C.ink, borderRadius: 2, paddingVertical: 9, paddingHorizontal: 14 },
  chooseBtnSm: { backgroundColor: C.ink, borderRadius: 2, paddingVertical: 7, paddingHorizontal: 12 },
  chooseBtnText: { color: '#fff', fontWeight: '700', fontSize: 13 },
  noFile: { color: C.faint, fontSize: 13 },
  chipOk: { color: C.ink, fontSize: 12.5, fontWeight: '700', flexShrink: 1 },
  link: { color: C.ink, fontWeight: '700', fontSize: 13, textDecorationLine: 'underline' },

  /* stats */
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    borderWidth: 1,
    borderColor: C.ink,
    borderRadius: 2,
    overflow: 'hidden',
  },
  statTile: {
    width: '50%',
    padding: 14,
    backgroundColor: C.panel,
    borderRightWidth: 1,
    borderBottomWidth: 1,
    borderColor: C.border,
  },
  statTileHi: { backgroundColor: '#f4f4f4' },
  statAccent: { position: 'absolute', left: 0, top: 0, bottom: 0, width: 3, backgroundColor: C.ink },
  statK: { fontSize: 10, color: C.muted, fontWeight: '700', letterSpacing: 0.8 },
  statV: { fontFamily: SERIF, fontWeight: '700', color: C.ink, marginTop: 5 },
  statVBig: { fontSize: 24 },
  statVSmall: { fontSize: 19 },

  /* buttons */
  btn: {
    borderWidth: 1,
    borderColor: C.ink,
    borderRadius: 2,
    paddingVertical: 11,
    paddingHorizontal: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnSm: { paddingVertical: 8, paddingHorizontal: 14 },
  btnPrimary: { backgroundColor: C.ink },
  btnPrimaryText: { color: '#fff', fontWeight: '700', fontSize: 13.5 },
  btnGhost: { backgroundColor: '#fff' },
  btnGhostText: { color: C.ink, fontWeight: '700', fontSize: 13.5 },
  btnDisabled: { backgroundColor: '#e6e6e6', borderColor: '#cfcfcf' },

  toolbar: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 14 },
  count: { color: C.muted, fontSize: 13, marginTop: 10 },

  /* student card */
  studentCard: { padding: 16 },
  studentTop: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  inpName: {
    flex: 1,
    fontFamily: SERIF,
    fontWeight: '700',
    fontSize: 16,
    color: C.ink,
    borderWidth: 1,
    borderColor: 'transparent',
    paddingVertical: 4,
    paddingHorizontal: 4,
  },
  iconBtn: { paddingHorizontal: 8, paddingVertical: 4 },
  iconBtnText: { color: C.faint, fontSize: 16 },
  rowLine: { flexDirection: 'row', alignItems: 'center', marginTop: 12, gap: 10 },
  colLabel: { fontSize: 10, fontWeight: '700', color: C.muted, letterSpacing: 0.6, width: 130 },
  inpRoll: {
    borderWidth: 1,
    borderColor: C.border2,
    borderRadius: 2,
    paddingVertical: 6,
    paddingHorizontal: 10,
    fontSize: 13,
    color: C.ink,
    minWidth: 80,
  },
  fileChosenRow: { flexDirection: 'row', alignItems: 'center', gap: 8, flex: 1 },
  fileChosen: { fontSize: 13, color: C.ink, flexShrink: 1 },
  studentBottom: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 16,
    gap: 10,
  },
  resultArea: { flex: 1 },
  resultCell: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  scorePill: { fontFamily: SERIF, fontWeight: '700', fontSize: 14, color: C.ink },
  gradeBadge: {
    width: 28,
    height: 28,
    borderRadius: 2,
    backgroundColor: C.ink,
    alignItems: 'center',
    justifyContent: 'center',
  },
  gradeBadgeText: { color: '#fff', fontFamily: SERIF, fontWeight: '800', fontSize: 13 },
  errorText: { color: C.ink, fontSize: 12.5, marginTop: 10, fontWeight: '600' },

  statusPill: {
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderColor: C.border2,
    backgroundColor: '#f2f2f2',
    paddingHorizontal: 9,
    paddingVertical: 3,
  },
  statusPillActive: { borderColor: C.ink, backgroundColor: '#fff' },
  statusPillText: { fontSize: 10.5, fontWeight: '700', color: C.muted, letterSpacing: 0.4 },
  statusPillTextActive: { color: C.ink },

  /* detail */
  back: { color: C.muted, fontWeight: '600', fontSize: 13, marginBottom: 12, fontFamily: SERIF },
  alertWarn: {
    borderWidth: 1.5,
    borderColor: C.ink,
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginBottom: 14,
    alignSelf: 'flex-start',
  },
  alertWarnText: { color: C.ink, fontSize: 12.5, fontWeight: '700' },
  footnote: { color: C.muted, fontSize: 12.5, marginTop: 14, fontStyle: 'italic' },

  qCard: { padding: 16 },
  qCardWarn: { backgroundColor: C.warnBg },
  qHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  qHeaderLeft: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  qno: { fontFamily: SERIF, fontWeight: '700', fontSize: 16, color: C.ink },
  qtype: {
    borderWidth: 1,
    borderColor: C.border2,
    borderRadius: 2,
    paddingHorizontal: 5,
    paddingVertical: 2,
  },
  qtypeMcq: { borderColor: C.ink },
  qtypeText: { fontSize: 9, fontWeight: '800', color: C.muted, letterSpacing: 0.5 },
  qtypeTextMcq: { color: C.ink },
  qMarkWrap: { alignItems: 'flex-end' },
  mark: { fontFamily: SERIF, fontWeight: '700', fontSize: 16, color: C.ink },
  markOf: { color: C.faint, fontWeight: '500', fontSize: 13 },
  meter: { height: 5, width: 70, backgroundColor: '#e2e2e2', marginTop: 6, overflow: 'hidden' },
  meterFill: { height: '100%', backgroundColor: C.ink },
  qFieldLabel: {
    fontSize: 10.5,
    fontWeight: '700',
    color: C.muted,
    letterSpacing: 0.5,
    marginTop: 12,
    marginBottom: 5,
  },
  confLow: { color: C.ink, fontWeight: '700' },
  confOk: { color: C.muted, fontWeight: '700' },
  inpArea: {
    borderWidth: 1,
    borderColor: C.border2,
    borderRadius: 2,
    padding: 10,
    fontSize: 13,
    color: C.ink,
    minHeight: 64,
    textAlignVertical: 'top',
  },
  mcqRow: { flexDirection: 'row', gap: 8 },
  mcqOpt: {
    borderWidth: 1,
    borderColor: C.border2,
    borderRadius: 2,
    width: 42,
    height: 38,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  mcqOptActive: { backgroundColor: C.ink, borderColor: C.ink },
  mcqOptText: { fontWeight: '700', color: C.ink, fontSize: 14 },
  mcqOptTextActive: { color: '#fff' },
  keyText: { color: C.muted, fontSize: 13, lineHeight: 19 },
  keyTextMcq: { fontWeight: '700', color: C.ink },
});
