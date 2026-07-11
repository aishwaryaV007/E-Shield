import axios from 'axios';
import Constants from 'expo-constants';

/**
 * Base URL of the ExamShield FastAPI backend (POST /api/v1/grade).
 *
 * Resolution order:
 *  1. EXPO_PUBLIC_API_URL env var — explicit override, always wins.
 *  2. Auto-derived from the Expo dev-server host. The phone loaded the JS
 *     bundle FROM that host, so it is guaranteed reachable — we just swap the
 *     Metro port (8081) for the backend port (8000). This means you never have
 *     to pass an IP: switch WiFi, hotspot, whatever, and it keeps working, as
 *     long as the backend runs on the same machine with --host 0.0.0.0.
 *  3. localhost — final fallback (works on iOS simulator / web).
 */
const BACKEND_PORT = 8000;

function deriveApiBase(): string {
  const override = process.env.EXPO_PUBLIC_API_URL?.replace(/\/$/, '');
  if (override) return override;

  // hostUri looks like "172.20.10.2:8081" in Expo Go dev.
  const hostUri =
    Constants.expoConfig?.hostUri ||
    (Constants.expoGoConfig as any)?.debuggerHost ||
    (Constants.manifest2 as any)?.extra?.expoGo?.debuggerHost;
  const host = hostUri?.split(':')[0];
  if (host && host !== 'localhost' && host !== '127.0.0.1') {
    return `http://${host}:${BACKEND_PORT}`;
  }
  return `http://localhost:${BACKEND_PORT}`;
}

export const API_BASE = deriveApiBase();

export type Answer = {
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

export type GradeSheet = {
  script_id: string;
  total_marks: number;
  max_total: number;
  percentage: number;
  mcq_marks: number;
  mcq_max: number;
  descriptive_marks: number;
  descriptive_max: number;
  low_confidence_count: number;
  answers: Answer[];
  elapsed_seconds?: number;
};

export type PickedFile = {
  uri: string;
  name: string;
  mimeType?: string;
};

/** Grade band matching the web frontend (backend/report percentage). */
export function gradeBand(p: number): string {
  if (p >= 90) return 'A+';
  if (p >= 80) return 'A';
  if (p >= 70) return 'B';
  if (p >= 60) return 'C';
  if (p >= 50) return 'D';
  if (p >= 40) return 'E';
  return 'F';
}

/**
 * Upload a handwritten answer-script (PDF) to the grader.
 * Optional answer key / question paper follow the same multipart contract
 * as the web app. Auth is bypassed server-side by default (DISABLE_AUTH=true).
 */
export async function gradeScript(
  file: PickedFile,
  opts: { answerKey?: PickedFile; questionPaper?: PickedFile; maxMarks?: number } = {}
): Promise<GradeSheet> {
  const fd = new FormData();
  // React Native FormData wants { uri, name, type } shaped parts.
  fd.append('file', {
    uri: file.uri,
    name: file.name || 'script.pdf',
    type: file.mimeType || 'application/pdf',
  } as any);
  fd.append('max_marks', String(opts.maxMarks ?? 2));
  if (opts.answerKey) {
    fd.append('answer_key', {
      uri: opts.answerKey.uri,
      name: opts.answerKey.name || 'answerkey.txt',
      type: opts.answerKey.mimeType || 'text/plain',
    } as any);
  }
  if (opts.questionPaper) {
    fd.append('question_paper', {
      uri: opts.questionPaper.uri,
      name: opts.questionPaper.name || 'questions.txt',
      type: opts.questionPaper.mimeType || 'text/plain',
    } as any);
  }

  const res = await axios.post<GradeSheet>(`${API_BASE}/api/v1/grade`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000, // OCR + scoring is slow (~seconds per script)
  });
  return res.data;
}

export type RescoreAnswer = {
  question_no: string;
  type: string;
  student_answer: string;
  answer_key: string;
  max_marks: number;
};

/** Re-grade after a human fixes the OCR text — fast, no OCR re-run. */
export async function rescore(
  answers: RescoreAnswer[],
  scriptId: string
): Promise<GradeSheet> {
  const res = await axios.post<GradeSheet>(
    `${API_BASE}/api/v1/rescore`,
    { answers, script_id: scriptId },
    { headers: { 'Content-Type': 'application/json' }, timeout: 60000 }
  );
  return res.data;
}
