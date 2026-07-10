import { Submission } from "@/types";

// This is a placeholder in-memory store so the prototype runs end-to-end
// without a database. Swap every function body here for a Supabase query
// (see README) once you wire up the real backend — the function
// signatures are designed to map 1:1 onto that change.

let submissions: Submission[] = [
  {
    id: "1",
    studentName: "Aisha Rao",
    examName: "Physics midterm — unit 4",
    status: "pending",
    questions: [
      {
        id: "q1",
        text: "State Newton's second law and give one real-world example.",
        answerKey: "F = ma; needs one concrete example",
        studentAnswer:
          "Force equals mass times acceleration. When you push an empty cart it speeds up faster than a full one, because it has less mass.",
        maxMarks: 5,
        mark: 4,
        confidence: "high",
        comment: "",
      },
      {
        id: "q2",
        text: "Derive the equation of motion v = u + at.",
        answerKey:
          "Full derivation from a = dv/dt with integration steps shown",
        studentAnswer: "a = (v - u) / t, so rearranging gives v = u + at.",
        maxMarks: 10,
        mark: 6,
        confidence: "medium",
        comment: "",
      },
      {
        id: "q3",
        text: "Explain the concept of inertia with an example.",
        answerKey:
          "Definition plus an everyday example (bus, seatbelt, tablecloth trick)",
        studentAnswer:
          "Inertia is the tendency of a body to resist a change in its state of motion. Example: passengers lurch forward when a moving bus stops suddenly.",
        maxMarks: 5,
        mark: 5,
        confidence: "high",
        comment: "",
      },
    ],
    query: null,
  },
  {
    id: "2",
    studentName: "Rohan Mehta",
    examName: "Physics midterm — unit 4",
    status: "published",
    questions: [
      {
        id: "q1",
        text: "State Newton's second law and give one real-world example.",
        answerKey: "F = ma; needs one concrete example",
        studentAnswer:
          "F=ma. A heavier truck needs more force to speed up than a car.",
        maxMarks: 5,
        mark: 5,
        confidence: "high",
        comment: "Clear and correct.",
      },
      {
        id: "q2",
        text: "Derive the equation of motion v = u + at.",
        answerKey:
          "Full derivation from a = dv/dt with integration steps shown",
        studentAnswer: "v = u + at (used directly from formula sheet).",
        maxMarks: 10,
        mark: 3,
        confidence: "low",
        comment:
          "Formula stated but no derivation shown — marks are for the final result only.",
      },
      {
        id: "q3",
        text: "Explain the concept of inertia with an example.",
        answerKey:
          "Definition plus an everyday example (bus, seatbelt, tablecloth trick)",
        studentAnswer:
          "Inertia means objects resist changing motion. Example: the tablecloth trick where dishes stay in place.",
        maxMarks: 5,
        mark: 5,
        confidence: "high",
        comment: "Nice example.",
      },
    ],
    query: {
      questionId: "q2",
      text: "I did write v=u+at correctly, why did I only get 3/10?",
      status: "open",
      reply: "",
    },
  },
];

export function listSubmissions(): Submission[] {
  return submissions;
}

export function getSubmission(id: string): Submission | undefined {
  return submissions.find((s) => s.id === id);
}

export function updateQuestion(
  submissionId: string,
  questionId: string,
  patch: Partial<Pick<Submission["questions"][number], "mark" | "comment">>
): Submission | undefined {
  const submission = getSubmission(submissionId);
  if (!submission) return undefined;
  const question = submission.questions.find((q) => q.id === questionId);
  if (!question) return undefined;
  Object.assign(question, patch);
  return submission;
}

export function publishSubmission(id: string): Submission | undefined {
  const submission = getSubmission(id);
  if (!submission) return undefined;
  submission.status = "published";
  return submission;
}

export function createQuery(
  submissionId: string,
  questionId: string,
  text: string
): Submission | undefined {
  const submission = getSubmission(submissionId);
  if (!submission) return undefined;
  submission.query = { questionId, text, status: "open", reply: "" };
  return submission;
}

export function replyToQuery(
  submissionId: string,
  reply: string
): Submission | undefined {
  const submission = getSubmission(submissionId);
  if (!submission || !submission.query) return undefined;
  submission.query.reply = reply;
  submission.query.status = "resolved";
  return submission;
}
