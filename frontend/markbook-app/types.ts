export type Confidence = "high" | "medium" | "low";

export interface Question {
  id: string;
  text: string;
  answerKey: string;
  studentAnswer: string;
  maxMarks: number;
  mark: number;
  confidence: Confidence;
  comment: string;
}

export interface Query {
  questionId: string;
  text: string;
  status: "open" | "resolved";
  reply: string;
}

export interface Submission {
  id: string;
  studentName: string;
  examName: string;
  status: "pending" | "published";
  questions: Question[];
  query: Query | null;
}
