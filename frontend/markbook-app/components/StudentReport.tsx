"use client";

import { useState } from "react";
import { Submission } from "@/types";
import { MarkCircle } from "./MarkCircle";
import * as api from "@/lib/api";

function total(s: Submission) {
  return s.questions.reduce((a, q) => a + q.mark, 0);
}
function maxTotal(s: Submission) {
  return s.questions.reduce((a, q) => a + q.maxMarks, 0);
}

export default function StudentReport({
  submissions,
  initialStudentId,
}: {
  submissions: Submission[];
  initialStudentId: string;
}) {
  const [all, setAll] = useState(submissions);
  const [studentId, setStudentId] = useState(initialStudentId);
  const [openFormFor, setOpenFormFor] = useState<string | null>(null);
  const [draft, setDraft] = useState("");

  const submission = all.find((s) => s.id === studentId);

  function patch(updated: Submission) {
    setAll((prev) => prev.map((s) => (s.id === updated.id ? updated : s)));
  }

  async function handleSend(questionId: string) {
    if (!submission || !draft.trim()) return;
    const updated = await api.sendQuery(submission.id, questionId, draft.trim());
    patch(updated);
    setDraft("");
    setOpenFormFor(null);
  }

  if (!submission) return null;

  return (
    <div>
      <div className="text-sm text-stone-500 mb-4">
        Viewing as
        <select
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          className="ml-2 text-sm border border-stone-300 rounded-md px-2 py-1"
        >
          {all.map((s) => (
            <option key={s.id} value={s.id}>
              {s.studentName}
            </option>
          ))}
        </select>
      </div>

      {submission.status !== "published" ? (
        <div className="bg-white border border-stone-200 rounded-xl p-10 text-center text-stone-500">
          <h3 className="font-serif text-lg text-stone-800">
            Your teacher is still reviewing this paper
          </h3>
          <p className="text-sm mt-1">
            You&apos;ll see your marks and feedback here once it&apos;s
            published.
          </p>
        </div>
      ) : (
        <>
          <div className="bg-white border border-stone-200 rounded-xl p-5 flex items-center gap-5 mb-4">
            <MarkCircle value={total(submission)} size={76} />
            <div>
              <h2 className="font-serif text-xl text-stone-800">
                {submission.examName}
              </h2>
              <p className="text-sm text-stone-500 mt-1">
                {total(submission)} out of {maxTotal(submission)} marks ·
                published
              </p>
            </div>
          </div>

          {submission.questions.map((q) => {
            const askedHere = submission.query?.questionId === q.id;
            return (
              <div
                key={q.id}
                className="bg-white border border-stone-100 rounded-lg p-4 mb-3.5"
              >
                <p className="text-sm font-medium text-stone-800 mb-2">
                  {q.text}
                </p>
                <p className="text-[13px] text-stone-500 mb-3">
                  <span className="font-medium text-stone-700">
                    Your answer —{" "}
                  </span>
                  {q.studentAnswer}
                </p>
                <div className="flex items-center gap-3">
                  <MarkCircle value={q.mark} size={40} />
                  <span className="text-sm text-stone-500">
                    out of {q.maxMarks}
                  </span>
                </div>
                {q.comment && (
                  <div className="text-xs text-stone-500 bg-stone-50 rounded-md px-2.5 py-2 mt-3">
                    {q.comment}
                  </div>
                )}

                {askedHere ? (
                  submission.query!.status === "resolved" ? (
                    <div className="text-sm bg-stone-50 rounded-md px-2.5 py-2 mt-3">
                      <span className="font-medium">Teacher reply: </span>
                      {submission.query!.reply}
                    </div>
                  ) : (
                    <p className="text-xs text-rose-700 mt-3">
                      Query sent — waiting for your teacher&apos;s reply
                    </p>
                  )
                ) : openFormFor === q.id ? (
                  <div className="mt-3">
                    <textarea
                      value={draft}
                      onChange={(e) => setDraft(e.target.value)}
                      placeholder="What would you like to ask?"
                      className="w-full border border-stone-300 rounded-md p-2 text-sm min-h-[40px]"
                    />
                    <button
                      onClick={() => handleSend(q.id)}
                      className="mt-1.5 bg-stone-900 text-white rounded-md px-3.5 py-1.5 text-xs font-medium hover:bg-stone-800"
                    >
                      Send
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setOpenFormFor(q.id)}
                    className="mt-3 border border-stone-300 rounded-md px-3 py-1.5 text-xs text-stone-600 hover:bg-stone-50"
                  >
                    Ask about this mark
                  </button>
                )}
              </div>
            );
          })}
        </>
      )}
    </div>
  );
}
