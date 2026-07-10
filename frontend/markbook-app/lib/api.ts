import { Submission } from "@/types";

export async function fetchSubmissions(): Promise<Submission[]> {
  const res = await fetch("/api/submissions", { cache: "no-store" });
  return res.json();
}

export async function updateQuestion(
  submissionId: string,
  questionId: string,
  patch: { mark?: number; comment?: string }
): Promise<Submission> {
  const res = await fetch(`/api/submissions/${submissionId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ questionId, ...patch }),
  });
  return res.json();
}

export async function publishSubmission(id: string): Promise<Submission> {
  const res = await fetch(`/api/submissions/${id}/publish`, {
    method: "POST",
  });
  return res.json();
}

export async function sendQuery(
  submissionId: string,
  questionId: string,
  text: string
): Promise<Submission> {
  const res = await fetch(`/api/submissions/${submissionId}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ questionId, text }),
  });
  return res.json();
}

export async function replyToQuery(
  submissionId: string,
  reply: string
): Promise<Submission> {
  const res = await fetch(`/api/submissions/${submissionId}/query`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reply }),
  });
  return res.json();
}
