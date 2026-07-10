"use client";

import { useState } from "react";
import { Submission } from "@/types";
import * as api from "@/lib/api";

const confidenceStyles: Record<string, string> = {
  high: "bg-emerald-50 text-emerald-700",
  medium: "bg-amber-50 text-amber-700",
  low: "bg-rose-50 text-rose-700",
};

function total(s: Submission) {
  return s.questions.reduce((a, q) => a + q.mark, 0);
}
function maxTotal(s: Submission) {
  return s.questions.reduce((a, q) => a + q.maxMarks, 0);
}

export default function TeacherDashboard({
  initialSubmissions,
}: {
  initialSubmissions: Submission[];
}) {
  const [submissions, setSubmissions] = useState(initialSubmissions);
  const [selectedId, setSelectedId] = useState(initialSubmissions[0]?.id);
  const [replyDraft, setReplyDraft] = useState("");

  const selected = submissions.find((s) => s.id === selectedId);

  function patchSubmission(updated: Submission) {
    setSubmissions((prev) =>
      prev.map((s) => (s.id === updated.id ? updated : s))
    );
  }

  async function handleMarkChange(questionId: string, mark: number) {
    if (!selected) return;
    // optimistic update
    patchSubmission({
      ...selected,
      questions: selected.questions.map((q) =>
        q.id === questionId ? { ...q, mark } : q
      ),
    });
    const updated = await api.updateQuestion(selected.id, questionId, {
      mark,
    });
    patchSubmission(updated);
  }

  async function handleCommentBlur(questionId: string, comment: string) {
    if (!selected) return;
    const updated = await api.updateQuestion(selected.id, questionId, {
      comment,
    });
    patchSubmission(updated);
  }

  async function handlePublish() {
    if (!selected) return;
    const updated = await api.publishSubmission(selected.id);
    patchSubmission(updated);
  }

  async function handleReply() {
    if (!selected || !replyDraft.trim()) return;
    const updated = await api.replyToQuery(selected.id, replyDraft.trim());
    patchSubmission(updated);
    setReplyDraft("");
  }

  if (!selected) return null;

  return (
    <div className="grid grid-cols-[280px_1fr] gap-5">
      {/* Submissions list */}
      <div className="bg-white border border-stone-200 rounded-xl h-fit">
        <h3 className="px-4 pt-4 pb-2 font-serif text-[15px] text-stone-800">
          Submissions
        </h3>
        {submissions.map((s) => {
          const pillLabel =
            s.query?.status === "open"
              ? "query"
              : s.status === "published"
              ? "published"
              : "pending";
          const pillClass =
            pillLabel === "query"
              ? "bg-rose-50 text-rose-700"
              : pillLabel === "published"
              ? "bg-emerald-50 text-emerald-700"
              : "bg-amber-50 text-amber-700";
          return (
            <button
              key={s.id}
              onClick={() => setSelectedId(s.id)}
              className={`w-full text-left px-4 py-3 border-t border-stone-100 flex items-center justify-between gap-2 hover:bg-stone-50 ${
                s.id === selectedId ? "bg-rose-50/60" : ""
              }`}
            >
              <span>
                <span className="block text-sm font-medium text-stone-800">
                  {s.studentName}
                </span>
                <span className="block text-xs text-stone-500 mt-0.5">
                  {s.examName}
                </span>
              </span>
              <span
                className={`text-[11px] font-medium px-2 py-1 rounded-full whitespace-nowrap ${pillClass}`}
              >
                {pillLabel}
              </span>
            </button>
          );
        })}
      </div>

      {/* Detail panel */}
      <div className="bg-white border border-stone-200 rounded-xl p-6">
        <div className="flex items-start justify-between pb-4 mb-5 border-b border-stone-100">
          <div>
            <h2 className="font-serif text-xl text-stone-800">
              {selected.studentName}
            </h2>
            <p className="text-sm text-stone-500 mt-1">
              {selected.examName} · total {total(selected)} /{" "}
              {maxTotal(selected)}
            </p>
          </div>
          <button
            onClick={handlePublish}
            disabled={selected.status === "published"}
            className={`rounded-lg px-4 py-2 text-sm font-medium ${
              selected.status === "published"
                ? "bg-emerald-600 text-white cursor-default"
                : "bg-stone-900 text-white hover:bg-stone-800"
            }`}
          >
            {selected.status === "published"
              ? "Published"
              : "Publish to student"}
          </button>
        </div>

        {selected.questions.map((q) => (
          <div
            key={q.id}
            className="border border-stone-100 rounded-lg p-4 mb-3.5"
          >
            <p className="text-sm font-medium text-stone-800 mb-2">
              {q.text}
            </p>
            <div className="text-xs text-stone-500 bg-stone-50 rounded-md px-2.5 py-2 mb-2.5">
              <span className="font-medium text-stone-700">
                Answer key —{" "}
              </span>
              {q.answerKey}
            </div>
            <p className="text-[13px] text-stone-500 leading-relaxed mb-3">
              {q.studentAnswer}
            </p>
            <div className="flex items-center gap-3.5 flex-wrap">
              <label className="text-xs text-stone-500">Marks</label>
              <input
                type="number"
                min={0}
                max={q.maxMarks}
                value={q.mark}
                onChange={(e) =>
                  handleMarkChange(
                    q.id,
                    Math.max(
                      0,
                      Math.min(q.maxMarks, Number(e.target.value) || 0)
                    )
                  )
                }
                className="w-14 font-mono text-sm text-center border border-stone-300 rounded-md py-1.5"
              />
              <span className="text-sm text-stone-500">/ {q.maxMarks}</span>
              <span
                className={`text-[11px] font-medium px-2 py-1 rounded-full ${
                  confidenceStyles[q.confidence]
                }`}
              >
                {q.confidence} confidence
              </span>
            </div>
            <textarea
              defaultValue={q.comment}
              onBlur={(e) => handleCommentBlur(q.id, e.target.value)}
              placeholder="Feedback for the student..."
              className="w-full mt-2.5 border border-stone-300 rounded-md p-2 text-sm min-h-[44px]"
            />
          </div>
        ))}

        {selected.query && (
          <div className="bg-rose-50 border border-rose-200 rounded-lg p-4 mt-2">
            <p className="text-[11px] font-medium text-rose-700 uppercase tracking-wide mb-1">
              Student query —{" "}
              {
                selected.questions.find(
                  (q) => q.id === selected.query!.questionId
                )?.text
              }
            </p>
            <p className="text-sm mb-2">{selected.query.text}</p>
            {selected.query.status === "resolved" ? (
              <div className="text-sm bg-white rounded-md px-2.5 py-2">
                <span className="font-medium">Your reply: </span>
                {selected.query.reply}
              </div>
            ) : (
              <>
                <textarea
                  value={replyDraft}
                  onChange={(e) => setReplyDraft(e.target.value)}
                  placeholder="Write a reply..."
                  className="w-full border border-rose-200 rounded-md p-2 text-sm min-h-[40px]"
                />
                <button
                  onClick={handleReply}
                  className="mt-2 bg-rose-700 text-white rounded-md px-3.5 py-1.5 text-xs font-medium hover:bg-rose-800"
                >
                  Send reply
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
